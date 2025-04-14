console.log("🔥 插件 content.js 注入成功！");

chrome.storage.sync.get("enabled", async ({ enabled }) => {
  if (!enabled) return;

  const selector = "#app > div > div:nth-child(4) > div > div > div > div.aui-formBox > div > div.aui-form-box > form > div > div:nth-child(3) > div.aui-code > img";
  const inputSelector = "#app > div > div:nth-child(4) > div > div > div > div.aui-formBox > div > div.aui-form-box > form > div > div:nth-child(3) > div.ant-form-item.css-dev-only-do-not-override-9m98ij > div > div > div > div > input";
  const buttonSelector = "#app > div > div:nth-child(4) > div > div > div > div.aui-formBox > div > div.aui-formButton > div:nth-child(1) > button";

  const waitForImgAndRecognize = () => {
    const observer = new MutationObserver(async () => {
      const imgElement = document.querySelector(selector);
      if (imgElement && imgElement.src.startsWith("data:image")) {
        observer.disconnect();

        // ✅ 调用本地模型识别服务
        try {
          const response = await fetch("http://localhost:5002/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: imgElement.src })
          });

          const { code: text } = await response.json();
          console.log("✅ 本地模型识别结果：", text);

          const input = document.querySelector(inputSelector);
          if (input) {
            input.value = text;
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
            console.log("✅ 已填入验证码");
          } else {
            console.warn("⚠️ 未找到验证码输入框！");
          }

          const loginBtn = document.querySelector(buttonSelector);
          if (loginBtn) {
            loginBtn.click();
            console.log("✅ 已自动点击登录按钮");
          } else {
            console.warn("⚠️ 未找到登录按钮！");
          }

        } catch (err) {
          console.error("❌ 调用本地模型识别失败：", err);
        }
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
  };

  waitForImgAndRecognize();
});
