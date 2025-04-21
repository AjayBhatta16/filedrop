import subprocess
import json

with open("./env.json", "r") as env_json, open("./env-var-deps.json", "r") as deps_json:
    env_vars_ref = json.loads(env_json.read())
    deps_ref = json.loads(deps_json.read())

    deps_base = deps_ref["shared-utils"]

    for fn_name, deps in deps_ref["functions"].items():
        fn_deps_list = '*'.join(deps_base).split('*')
        for dep in deps:
            fn_deps_list.append(dep)
        
        fn_env_str = "Variables={" + (",".join(f"{dep}={env_vars_ref[dep]}" for dep in fn_deps_list)) + "}"
        env_update_cmd = f"aws lambda update-function-configuration --function-name {fn_name} --environment {fn_env_str}"

        print(env_update_cmd)

        subprocess.run(env_update_cmd, shell=True)