-- Proposal R-02 untuk Claude: ganti hanya fungsi ini setelah membaca source terbaru.
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
