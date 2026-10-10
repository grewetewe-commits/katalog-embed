"""Regression checks for evaluation integrity; fixtures are not runtime catalog data."""
import unittest
import numpy as np

from otak import (bagian_kreator, fitb_ketat, negatif_slot, pusat_slot_latih, latih,
                  periksa_model_sebelum_ekspor)


class TrainingEvaluationTests(unittest.TestCase):
    def test_creator_split_is_stable_and_disjoint(self):
        groups = {name: set() for name in ('latih', 'pilih', 'uji')}
        for i in range(1000):
            key = 'creator-' + str(i)
            part = bagian_kreator(key)
            self.assertEqual(part, bagian_kreator(key))
            groups[part].add(key)
        self.assertTrue(all(len(group) > 100 for group in groups.values()))
        self.assertFalse(groups['latih'] & groups['pilih'])
        self.assertFalse(groups['latih'] & groups['uji'])
        self.assertFalse(groups['pilih'] & groups['uji'])

    def test_exhausted_slot_returns_none(self):
        self.assertIsNone(negatif_slot(np.arange(30), set(range(30)),
                                      np.random.default_rng(1), 24))

    def test_single_remaining_training_negative(self):
        result = negatif_slot(np.arange(30), set(range(29)),
                               np.random.default_rng(1), 24)
        self.assertEqual(result, [29] * 24)

    def test_insufficient_unique_candidates_returns_none(self):
        self.assertIsNone(negatif_slot(np.arange(30), set(range(28)),
                                      np.random.default_rng(1), 3, unik=True))

    def test_unique_candidates_exclude_outfit(self):
        result = negatif_slot(np.arange(1000), set(range(800)),
                               np.random.default_rng(1), 7, unik=True)
        self.assertEqual(len(set(result)), 7)
        self.assertTrue(all(x >= 800 for x in result))

    def test_tied_vectors_are_not_correct(self):
        fz = np.ones((40, 32), dtype=np.float32)
        self.assertEqual(fitb_ketat(fz, [('a', [(0, 's'), (1, 's'), (2, 's')])],
                                   {'s': np.arange(40)}), (0.0, 3))

    def test_non_finite_scores_are_not_correct(self):
        fz = np.full((40, 32), np.nan, dtype=np.float32)
        self.assertEqual(fitb_ketat(fz, [('a', [(0, 's'), (1, 's'), (2, 's')])],
                                   {'s': np.arange(40)}), (0.0, 3))

    def test_full_slot_test_skips_without_hanging(self):
        fz = np.ones((30, 32), dtype=np.float32)
        self.assertEqual(fitb_ketat(fz, [('a', [(i, 's') for i in range(30)])],
                                   {'s': np.arange(30)}), (0.0, 0))

    def test_centering_does_not_use_held_out_features(self):
        features = np.array([[1., 2.], [3., 4.], [1e6, 1e6]])
        means = pusat_slot_latih(features, np.array(['a', 'a', 'a']), [0, 1])
        np.testing.assert_array_equal(means['a'], [2., 3.])

    def test_empty_training_centering_fails(self):
        with self.assertRaises(ValueError):
            pusat_slot_latih(np.zeros((3, 2)), np.array(['a', 'a', 'a']), [])

    def valid_export(self):
        return dict(ids=list(range(32)), fz=np.ones((32, 32), dtype=np.float32),
                    hasil=dict(layak=True, fitb_dipakai=0.5, soal_uji=150))

    def test_missing_or_failed_model_cannot_replace_snapshot(self):
        with self.assertRaises(RuntimeError):
            periksa_model_sebelum_ekspor(None)
        candidate = self.valid_export()
        candidate['hasil']['layak'] = False
        with self.assertRaises(RuntimeError):
            periksa_model_sebelum_ekspor(candidate)

    def test_under_tested_model_cannot_replace_snapshot(self):
        candidate = self.valid_export()
        candidate['hasil']['soal_uji'] = 149
        with self.assertRaises(RuntimeError):
            periksa_model_sebelum_ekspor(candidate)

    def test_malformed_vectors_cannot_replace_snapshot(self):
        for bad in [np.zeros((32, 31)), np.full((32, 32), np.nan)]:
            candidate = self.valid_export()
            candidate['fz'] = bad
            with self.assertRaises(RuntimeError):
                periksa_model_sebelum_ekspor(candidate)

    def test_valid_model_passes_export_guard(self):
        periksa_model_sebelum_ekspor(self.valid_export())

    def test_training_smoke_preserves_export_contract(self):
        import torch
        torch.set_num_threads(2)
        rng = np.random.default_rng(17)
        ids = list(range(1, 121))
        slots = {i: ('Shirt' if i <= 40 else 'Pants' if i <= 80 else 'Hat') for i in ids}
        emb = {i: rng.normal(size=512).astype(np.float32) for i in ids}
        state = dict(meta={}, tolak={}, outfit={})
        for i in range(160):
            state['outfit'][str(i)] = dict(K='creator-' + str(i),
                Sh=1 + i % 40, Pa=41 + (i * 7) % 40,
                A=[[81 + (i * 11) % 40, 1]])
        result = latih(state, emb, slots, langkah_uji=2, batas_detik=30)
        self.assertIsNotNone(result)
        self.assertEqual(result['fz'].shape, (120, 32))
        self.assertTrue(np.isfinite(result['fz']).all())
        metrics = result['hasil']
        self.assertEqual(metrics['evaluasi_versi'], 2)
        self.assertFalse(metrics['seri_benar'])
        self.assertGreaterEqual(metrics['outfit_pemilihan'], 3)
        self.assertGreaterEqual(metrics['outfit_uji'], 3)
        self.assertLessEqual(metrics['fitb_dipakai'], 1)


if __name__ == '__main__':
    unittest.main()
