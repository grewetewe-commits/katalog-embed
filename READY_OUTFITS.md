# Public complete outfit references

`ready_outfits.mjs` reads actual public Roblox Look IDs and publicly readable saved avatar outfits. It stores exact asset IDs, original body parts, six scales, skin colors, rigid accessory adjustments, and layered clothing order/puffiness. Look IDs remain decimal strings because many exceed JavaScript's safe integer range.

The supplied snapshot has 99 Marketplace Look compositions and 7 additional saved public outfits. Saved outfits are not represented as published Marketplace Looks. The number of collected records is not the global Marketplace count.

## Collection

- `data/ready_outfit_sources.json`: observed Look IDs and public creator IDs, never guessed share codes.
- `data/ready_outfit_cursor.json`: resumable pagination tokens, pending outfit details, refresh times and creator rotation.
- `bank/ready_outfits.json`: bounded bank, maximum 4,000 complete references.
- `data/ready_outfit_report.json`: actual requests, accepted records and failures.
- Public GET requests only, no account cookies or new credentials. Request pacing, bounded retries, 20 second timeout, 12 minute deadline, at most 90 requests per scheduled run. HTTP 429 work remains queued.
- Pagination advances only after discovered detail work is checkpointed. Incomplete avatar definitions are rejected.
- GitHub collection runs every six hours on main; it does not run independently in every game server.

`ready_import.py` feeds these compositions into the existing local CLIP/training pipeline. Creator grouping uses a stable hash where available. It preserves original body and layering in model exports. It adds no paid AI API or service.

## Studio integration

The local Starter snapshot loads immediately. Server-only refresh reads the public GitHub manifest through jsDelivr with raw GitHub fallback every six hours. Failed reads retain the last valid bank. `ReadyLookSource` supplies data to `OutfitDasarEngine`; `WholeOutfitKit` checks retained composition, complete shoe pairs, body context, and selected items before final outfit ranking. Theme, gender, budget and sale validation continue in the existing pipeline. Original reference body data is context; the player's selected body is applied to the result.

Favorite storage and production previews preserve layer order/puffiness through `PenyesuaianKit`. The disabled per-server creator crawler has been removed. Body compatibility choices remain available for an incompatible selected layered garment.

## Limits

Marketplace widget discovery may require login. No verified anonymous endpoint for exhaustive global Marketplace Look enumeration/count is established. Public saved outfit pagination expands the bank beyond widget results, but cannot prove complete Marketplace coverage. Source outfits authored by people are references, not guaranteed aesthetic labels. Existing visual gates still require live visual evaluation; retaining a composition alone does not certify that it fits a new body.

## Checks

Run `node --test test_ready_outfits.mjs`, `python -m unittest test_ready_import`, and `python -m py_compile otak.py ready_import.py`. These verify data integrity and recovery, not universal visual quality. The scheduled collector uses public repository Actions and public Roblox APIs; no plan upgrades or chargeable API subscriptions are configured by this change. Availability remains subject to provider quotas.
