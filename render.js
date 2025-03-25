const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const inputDir = "./output_html";
const outputDir = "./output_image";

// output_image 폴더가 없다면 생성
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir);
}

(async () => {
  const browser = await puppeteer.launch();
  const files = fs
    .readdirSync(inputDir)
    .filter((file) => file.endsWith(".html"));

  for (const file of files) {
    const filePath = path.resolve(inputDir, file);
    const page = await browser.newPage();

    await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 2 });
    await page.goto("file://" + filePath, { waitUntil: "networkidle0" });
    await page.emulateMediaType("print"); // 이 줄 추가
    await page.evaluate(() => {
      const saveBtn = document.querySelector("#save-btn");
      if (saveBtn) saveBtn.classList.add("render-hidden");
    });

    // 특정 영역만 캡처: .product-area-wrapper
    const element = await page.$(".product-area-wrapper");

    if (!element) {
      console.warn(`⚠️ .product-area-wrapper not found in ${file}`);
      continue;
    }

    const boundingBox = await element.boundingBox();
    if (!boundingBox) {
      console.warn(`⚠️ Could not calculate bounding box for ${file}`);
      continue;
    }

    const imageFile = file.replace(".html", ".png");
    await page.screenshot({
      path: path.join(outputDir, imageFile),
      clip: {
        x: boundingBox.x,
        y: boundingBox.y,
        width: boundingBox.width,
        height: boundingBox.height,
      },
    });

    console.log(`✅ Rendered: ${imageFile}`);
    await page.close();
  }

  await browser.close();
})();
