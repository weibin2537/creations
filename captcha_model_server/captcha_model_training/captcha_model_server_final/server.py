from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import torch
from model import CaptchaResNet, preprocess_image, decode_prediction
from flask_cors import CORS  # ✅ 新增

app = Flask(__name__)
CORS(app)  # ✅ 解决跨域问题
# ✅ 实例化模型结构，并加载 state_dict 权重
model = CaptchaResNet()
model.load_state_dict(torch.load("captcha_model.pth", map_location="cpu"))
model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    if not data or "image" not in data:
        return jsonify({"error": "Missing image"}), 400

    try:
        # 获取 base64 字符串部分
        img_data = data["image"].split(",")[-1]
        image = Image.open(io.BytesIO(base64.b64decode(img_data))).convert("L")
        input_tensor = preprocess_image(image).unsqueeze(0)

        # 模型推理
        with torch.no_grad():
            output = model(input_tensor)
            code = decode_prediction(output)

        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
