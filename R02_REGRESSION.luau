-- R-02 isolated regression. Actual registration/Peek/PeekAny/Fold source captured 2026-10-15.
-- Synthetic metadata only. No live require, DataStore, network, or Instance mutation.
local before = [==[function M.DaftarkanPasanganSepatu(left, right, bundle)
	if type(left) ~= "number" or type(right) ~= "number" or type(bundle) ~= "number" then return end
	pasanganSepatu[left], pasanganSepatu[right] = {id = right, bundle = bundle}, {id = left, bundle = bundle}
end]==]
local after = [==[-- Proposal R-02 untuk Claude: ganti hanya fungsi ini setelah membaca source terbaru.
-- Tidak menjalankan request/require, tidak mengganti metadata snapshot dengan klaim live.
function M.DaftarkanPasanganSepatu(left, right, bundle)
	local function validId(id)
		return type(id) == "number" and id > 0 and id < 2^53 and id % 1 == 0
	end
	if not validId(left) or not validId(right) or not validId(bundle) or left == right then return end

	local function record(other, prior)
		local result = {id = other, bundle = bundle}
		-- Metadata dapat diwariskan melalui __index, jadi table.clone(prior) tidak cukup.
		-- Jangan membawa harga/status lama bila identitas bundle atau salah satu kaki berubah.
		if type(prior) == "table" and prior.id == other and prior.bundle == bundle
			and prior.kiri == left and prior.kanan == right then
			result.kiri, result.kanan = prior.kiri, prior.kanan
			result.harga, result.jual = prior.harga, prior.jual
			result.nama, result.kreator = prior.nama, prior.kreator
		end
		return result
	end
	local previousLeft, previousRight = pasanganSepatu[left], pasanganSepatu[right]
	pasanganSepatu[left], pasanganSepatu[right] = record(right, previousLeft), record(left, previousRight)
end
]==]
local peekSource = [==[function K.Peek(id)
	local e = cache[id]
	return e and e.expires > os.clock() and e.pair or nil
end
-- rev 26 (Claude): pasangan dari data bundle GitHub (meta/sepatu.json, diambil dari katalog resmi saat panen) untuk sepatu
-- yang DIPILIHKAN otomatis oleh desainer. Pemeriksaan live (Peek) tetap didahulukan. Harga/status bisa sedikit basi;
-- pembelian tetap lewat prompt resmi Roblox, jadi bundle yang sudah tidak dijual hanya gagal dibeli, tidak merugikan.
local OG = nil
function K.PeekAny(id)
	local live = K.Peek(id)
	if live then return live end
	if not OG then
		local ok, m = pcall(require, script.Parent:FindFirstChild("OtakGayaEngine"))
		if not ok then return nil end
		OG = m
	end
	local p = OG.PasanganSepatu and OG.PasanganSepatu(id)
	if not p or not positive(p.kiri) or not positive(p.kanan) or type(p.harga) ~= "number" then return nil end
	return {id = p.id, assetType = (id == p.kiri) and 71 or 70, bundle = p.bundle, left = p.kiri, right = p.kanan,
		price = p.harga, forSale = p.jual == true, nameBundle = p.nama, creator = p.kreator, source = "GITHUB_BUNDLE"}
end
]==]
local foldSource = [==[function K.Fold(od)
	if type(od.Breakdown) ~= "table" then return end
	local present = {}
	for _, a in ipairs(od.DaftarAksesoris or {}) do present[a.AssetId] = true end
	local rows, done = {}, {}
	for _, row in ipairs(od.Breakdown) do
		local p = K.PeekAny(row.Id)
		if p and present[p.left] and present[p.right] and type(p.price) == "number" then
			if not done[p.bundle] then
				done[p.bundle] = true
				rows[#rows + 1] = {Id = p.bundle, Bundle = true, Kategori = "Sepatu", AssetIds = {p.left, p.right},
					Nama = p.nameBundle or "Sepasang sepatu", Creator = p.creator or row.Creator,
					Harga = math.max(0, p.price), Dijual = p.forSale}
			end
		else rows[#rows + 1] = row end
	end
	local total = 0
	for _, row in ipairs(rows) do total += math.max(0, tonumber(row.Harga) or 0) end
	od.Breakdown, od.HargaTotal = rows, total
end

]==]

local function context(registration)
	local factory = assert(loadstring([[
		local pasanganSepatu, M, K, cache = {}, {}, {}, {}
		local clock = 0
		local os = {clock = function() return clock end}
		local function positive(v)
			return type(v) == "number" and v > 0 and v < 2^53 and v % 1 == 0
		end
		function M.PasanganSepatu(id) return pasanganSepatu[id] end
		local require = function() return M end
		local script = {Parent = {FindFirstChild = function() return {} end}}
		]] .. registration .. "\n" .. peekSource .. "\n" .. foldSource .. [[
		return {M=M, K=K, pairs=pasanganSepatu, cache=cache,
			clock=function(t) clock=t end}
	]]))
	local c=factory()
	local meta={bundle=301,kiri=101,kanan=102,harga=75,jual=true,nama="Pair A",kreator="Fixture"}
	c.pairs[101]=setmetatable({id=102},{__index=meta})
	c.pairs[102]=setmetatable({id=101},{__index=meta})
	c.metadata=meta
	return c
end
local function live(c)
	c.cache[101]={expires=600,pair={id=102,bundle=301,left=101,right=102,price=99,forSale=false,source="ROBLOX_BUNDLE"}}
end
local function same(c) c.M.DaftarkanPasanganSepatu(101,102,301) end
local function suite(registration)
	local r={total=0,passed=0,failed=0,cases={}}
	local function case(name,fn)
		local ok,err=pcall(fn,context(registration))
		r.total+=1
		if ok then r.passed+=1 else r.failed+=1 end
		table.insert(r.cases,{name=name,passed=ok,error=not ok and tostring(err) or nil})
	end
	case("snapshot_initial_fallback",function(c)
		assert(c.K.PeekAny(101).price==75 and c.K.PeekAny(102).assetType==70)
	end)
	case("same_pair_keeps_inherited_metadata",function(c)
		same(c)
		for _,id in ipairs({101,102}) do
			local p=c.M.PasanganSepatu(id)
			assert(p.kiri==101 and p.kanan==102 and p.harga==75 and p.jual==true and p.nama=="Pair A" and p.kreator=="Fixture")
		end
	end)
	case("live_still_wins",function(c)
		live(c) same(c)
		local p=c.K.PeekAny(101)
		assert(p.price==99 and p.forSale==false and p.source=="ROBLOX_BUNDLE")
	end)
	case("expiry_599_to_600",function(c)
		live(c) same(c) c.clock(599)
		assert(c.K.PeekAny(101).source=="ROBLOX_BUNDLE")
		c.clock(600)
		local p=c.K.PeekAny(101)
		assert(p and p.price==75 and p.source=="GITHUB_BUNDLE")
	end)
	case("eviction_restores_snapshot_fallback",function(c)
		live(c) same(c) c.cache[101]=nil
		assert(c.K.PeekAny(101) and c.K.PeekAny(101).price==75)
	end)
	case("repeat_registration_idempotent",function(c)
		same(c) same(c)
		assert(c.K.PeekAny(102) and c.K.PeekAny(102).right==102)
	end)
	case("offsale_false_preserved",function(c)
		c.metadata.jual=false same(c)
		local p=c.K.PeekAny(101)
		assert(p and p.forSale==false)
	end)
	case("zero_price_preserved",function(c)
		c.metadata.harga=0 same(c)
		local p=c.K.PeekAny(101)
		assert(p and p.price==0)
	end)
	case("changed_bundle_no_old_price",function(c)
		c.M.DaftarkanPasanganSepatu(101,102,302)
		assert(c.M.PasanganSepatu(101).bundle==302 and c.K.PeekAny(101)==nil and c.K.PeekAny(102)==nil)
	end)
	case("changed_partner_no_old_price",function(c)
		c.M.DaftarkanPasanganSepatu(101,103,301)
		assert(c.M.PasanganSepatu(101).id==103 and c.K.PeekAny(101)==nil and c.K.PeekAny(103)==nil)
	end)
	case("swapped_sides_no_old_price",function(c)
		c.M.DaftarkanPasanganSepatu(102,101,301)
		assert(c.K.PeekAny(101)==nil and c.K.PeekAny(102)==nil)
	end)
	case("new_pair_has_mapping_only",function(c)
		c.M.DaftarkanPasanganSepatu(201,202,401)
		assert(c.M.PasanganSepatu(201).id==202 and c.K.PeekAny(201)==nil)
	end)
	case("wrong_record_identity_no_copy",function(c)
		c.pairs[101]=setmetatable({id=999},{__index=c.metadata})
		same(c)
		assert(c.M.PasanganSepatu(101).id==102 and c.K.PeekAny(101)==nil)
	end)
	case("invalid_ids_do_not_mutate",function(c)
		local prev=c.pairs[101]
		for _,args in ipairs({{101,101,301},{101,102,0},{101,102,-1},{101,102,1.5},{101,102,math.huge},{101,102,2^53},{101,102,0/0}}) do
			c.M.DaftarkanPasanganSepatu(table.unpack(args))
			assert(c.pairs[101]==prev)
		end
	end)
	case("source_metadata_not_mutated",function(c)
		local prev=c.pairs[101] same(c)
		assert(prev.harga==75 and c.metadata.harga==75 and rawget(prev,"harga")==nil)
	end)
	case("fold_pair_one_bundle_after_expiry",function(c)
		live(c) same(c) c.clock(600)
		local od={DaftarAksesoris={{AssetId=101},{AssetId=102}},
			Breakdown={{Id=101,Harga=0},{Id=102,Harga=0},{Id=900,Harga=20}}}
		c.K.Fold(od)
		assert(#od.Breakdown==2 and od.Breakdown[1].Bundle==true and od.Breakdown[1].Id==301 and od.HargaTotal==95)
	end)
	case("fold_single_shoe_does_not_claim_pair",function(c)
		same(c)
		local od={DaftarAksesoris={{AssetId=101}},Breakdown={{Id=101,Harga=0}}}
		c.K.Fold(od)
		assert(#od.Breakdown==1 and not od.Breakdown[1].Bundle)
	end)
	return r
end
return {before=suite(before),proposal=suite(after)}
