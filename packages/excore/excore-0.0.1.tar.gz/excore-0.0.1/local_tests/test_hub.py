from core import hub

model = hub.load('asthestarsfalll/BiSeNet-MegEngine:main', 'bisenetv1', git_host='github.com', pretrained=True, use_cache=False)
print(model)
