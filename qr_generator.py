import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont
import uuid
from dataclasses import dataclass
import os
import io
import base64


@dataclass
class QRCodeConfiguration:
    """QR Configuration Class"""

    front_color: tuple = (48, 41, 76)  # (158, 145, 165)
    middle_color: tuple = (48, 41, 76)  # (74, 62, 76)
    back_color: tuple = (255, 255, 255)
    logo_path: tuple = os.path.join(os.getcwd(), "logo.png")
    output_directory: tuple = os.path.join(os.getcwd(), "output")


class QRGenerator:
    """Class that is responsible for creating the QR Code in Deerhack theme"""

    def __init__(
        self, id: str, first_name: str, last_name: str, email: str, team: str
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.team = team
        self.qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
        )
        self.image = None
        self.id = id

    def style(self) -> None:
        """Adds the relevant style to the final image object, change size, color etc here.."""
        self.image = self.qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            # color_mask=RadialGradiantColorMask(
            #     # QRCodeConfiguration.front_color,
            #     # QRCodeConfiguration.middle_color,
            #     # QRCodeConfiguration.front_color,
            # ),
            color_mask=SolidFillColorMask(
                QRCodeConfiguration.back_color, QRCodeConfiguration.front_color
            ),
            # embeded_image_path=QRCodeConfiguration.logo_path,
        )

    def data(self) -> None:
        """Responsible for Setting the data to the image, add fields, etc.. here"""
        self.qr.add_data(
            {
                "First-Name": self.first_name,
                "Last-Name": self.last_name,
                # "Name":f"{self.first_name} {self.last_name}",
                # "Email": self.email,
                "Team": self.team,
                "ID": str(self.id),
                # "Message": "Any Tampering with the QR code or the Food system will result in direct elimination :)",
            },
            20,
        )

    def save(self) -> None:
        """Saves Image to drive, change file name,etc here..."""
        path = os.path.join(
            QRCodeConfiguration.output_directory,
            f"{self.first_name}_{self.last_name}.png",
        )
        self.image.save(path, "png")
        print(type(self.image))

    def get_base64_of_qr_image(self):
        """Returns the base 64 data of the qr image object"""
        image_stream = io.BytesIO()
        self.image.save(image_stream, format="png")
        image_stream.seek(0)
        binary_data = image_stream.getvalue()
        base_64_data = base64.b64encode(binary_data).decode("utf-8")
        return base_64_data

    def add_text(self):
        img = Image.new("RGB", (490, 543), color=QRCodeConfiguration.back_color)
        img.paste(self.image)

        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("font/Poppins-Bold.ttf", 40)

        text = f"{self.first_name.title()} {self.last_name.title()}"

        _, _, w, h = draw.textbbox((0, 0), text, font=font)

        draw.text(
            ((490 - w) / 2, (510 - h)),
            text,
            font=font,
            fill=QRCodeConfiguration.front_color,
        )

        self.image = img

    def main(self) -> str:
        """Main Method, Responsible for creating all qr codes, rearrange the execution structure here..
        Returns the bs4 of the image that is just saved.
        """
        self.data()
        self.style()

        # self.add_text()

        self.save()
        return self.get_base64_of_qr_image()


if __name__ == "__main__":
    gen = QRGenerator(
        str(uuid.uuid4()),
        "Amrit",
        "Pudasaini",
        "amrit.pudasaini@gmeial.com",
        "Hacker",
    )
    gen.main()
