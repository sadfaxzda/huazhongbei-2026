import sys

libs = [
    ("numpy", "np"),
    ("scipy", None),
    ("sympy", None),
    ("pandas", "pd"),
    ("matplotlib", None),
    ("seaborn", "sns"),
    ("plotly", None),
    ("sklearn", "scikit-learn"),
    ("pulp", None),
    ("cvxpy", "cp"),
    ("networkx", "nx"),
    ("statsmodels", None),
    ("jupyterlab", None),
]

print(f"Python {sys.version}\n")
print(f"{'库':<20} {'状态':<8} 版本")
print("-" * 45)

all_ok = True
for entry in libs:
    name = entry[0]
    label = entry[1] if entry[1] else name
    try:
        mod = __import__(name)
        ver = getattr(mod, "__version__", "unknown")
        print(f"{label:<20} {'OK':<8} {ver}")
    except ImportError as e:
        print(f"{label:<20} {'FAIL':<8} {e}")
        all_ok = False

print("-" * 45)
if all_ok:
    print("所有库均可正常导入，环境配置完成！")
else:
    print("部分库导入失败，请检查安装。")
