# qr_generator.py
import qrcode
import os

def generate_qr(mart_name: str, tracking_url: str) -> str:
    """
    트래킹 URL을 QR 코드로 변환하여 output_qr 디렉토리에 저장하고,
    해당 파일 경로를 반환합니다.
    """
    safe_mart_name = "".join(c for c in mart_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    qr_path = os.path.join("output_qr", f"{safe_mart_name}.png")

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=1
    )
    qr.add_data(tracking_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    return qr_path
