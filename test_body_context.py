"""Run production parser/importer body tests without loading a model or network."""
import ast
import copy
import json
import math
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
results = []

for repo in (".",):
    source = (ROOT / repo / "otak.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    env = {"math": math, "time": time}
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("ASET_KE_ACC", "LAYERED") for t in n.targets):
            exec(compile(ast.Module(body=[copy.deepcopy(n)], type_ignores=[]), "constants", "exec"), env)
    for name in ("hash_kanonik", "seed_dari_avatar"):
        exec(compile(ast.Module(body=[copy.deepcopy(functions[name])], type_ignores=[]), name, "exec"), env)
    seed = env["seed_dari_avatar"]
    tests = []

    def check(name, condition):
        tests.append({"name": name, "pass": bool(condition)})

    avatar = {"playerAvatarType": "R15", "assets": [
        {"id": 101, "assetType": {"id": 11}},
        {"id": 102, "assetType": {"id": 12}},
        {"id": 103, "assetType": {"id": 41}}],
        "scales": dict(height=1, width=1, depth=1, head=1, proportion=0, bodyType=0)}
    first = seed(avatar)
    fields = ("Head", "Torso", "LeftArm", "RightArm", "LeftLeg", "RightLeg")
    check("explicit default scales retained", first["SC"] == [1, 1, 1, 1, 0, 0])
    check("official body default IDs retained", first["BP"] == dict.fromkeys(fields, 0))
    custom = copy.deepcopy(avatar)
    for asset_type, field in ((79, "Head"), (27, "Torso"), (29, "LeftArm"), (28, "RightArm"), (30, "LeftLeg"), (31, "RightLeg")):
        custom["assets"].append({"id": asset_type + 1000, "assetType": {"id": asset_type}})
        check("official body type " + field, seed(custom)["BP"][field] == asset_type + 1000)
    unknown = copy.deepcopy(avatar)
    del unknown["scales"]
    del unknown["playerAvatarType"]
    check("unknown body IDs and scales not fabricated", "BP" not in seed(unknown) and "SC" not in seed(unknown))
    check("unknown rig not fabricated", "R" not in seed(unknown))
    for value in (True, float("nan"), float("inf"), -1, 0, 3):
        bad = copy.deepcopy(avatar)
        bad["scales"]["width"] = value
        check("invalid scale " + str(value), "SC" not in seed(bad))
    bad = copy.deepcopy(custom)
    bad["assets"][-1]["id"] = True
    check("boolean body ID rejected", "BP" not in seed(bad))
    bad["assets"][-1]["id"] = 2**53
    check("oversize body ID rejected", "BP" not in seed(bad))
    partial = copy.deepcopy(avatar)
    del partial["scales"]["head"]
    check("partial scales remain unknown", "SC" not in seed(partial))
    importer = next(n for n in functions["ambil_dari_roblox"].body if isinstance(n, ast.FunctionDef) and n.name == "masukkan")
    state = {"outfit": {}, "tolak": {}}
    env.update(st=state, ACC_KE_ASET={v: k for k, v in env["ASET_KE_ACC"].items()})
    exec(compile(ast.Module(body=[copy.deepcopy(importer)], type_ignores=[]), "production-importer", "exec"), env)
    record = {"Sh": 101, "Pa": 102, "A": [[103, 2]], "BP": seed(custom)["BP"], "SC": [1, .75, .8, 1, 0, 1], "R": "R15"}
    env["masukkan"]([record], "studio")
    imported = next(iter(state["outfit"].values()))
    check("anonymous feedback retains BP", imported["BP"] == record["BP"])
    check("anonymous feedback retains SC", imported["SC"] == record["SC"])
    check("anonymous feedback retains rig", imported["R"] == record["R"])
    env["st"] = {"outfit": {}, "tolak": {}}
    invalid = copy.deepcopy(record)
    invalid["BP"] = {"Head": 0}
    invalid["SC"][1] = float("nan")
    env["masukkan"]([invalid], "studio")
    imported_bad = next(iter(env["st"]["outfit"].values()))
    check("import rejects incomplete or nonfinite context", "BP" not in imported_bad and "SC" not in imported_bad)
    exporter = functions["ekspor"]
    allowed = next(n for n in ast.walk(exporter) if isinstance(n, ast.Tuple) and any(isinstance(x, ast.Constant) and x.value == "Sh" for x in n.elts) and any(isinstance(x, ast.Constant) and x.value == "BCn" for x in n.elts))
    check("export includes body context", "BP" in ast.literal_eval(allowed) and "SC" in ast.literal_eval(allowed))
    results.append({"repo": repo, "total": len(tests), "failed": sum(not t["pass"] for t in tests), "tests": tests})

report = {"scope": "Actual production parser/importer functions; no network/training", "results": results}
print(json.dumps(report))
assert all(r["failed"] == 0 for r in results)
