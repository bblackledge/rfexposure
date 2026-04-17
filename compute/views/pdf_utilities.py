import logging

import os
import datetime
import uuid
from urllib.parse import urlparse

from django.contrib.staticfiles import finders
from django.conf import settings as django_settings
from xhtml2pdf import pisa
from pdf2image import convert_from_path
from PIL import Image

from exposure import settings

logger = logging.getLogger('app.global')

class PDFUtilities(object):
    """ PDF and Image Extraction-Resizing Utilities and Creation Class"""

    def __init__(self):
        self.error = None
        self.error_message = ""
        self.unique_id = ""

    @staticmethod
    def generate_unique_filename(base_name="exposure_report"):
        """
        Generate Unique Filename for New PDF Report Generated
        :param base_name: str
        :return: str
        :state: Stable
        """

        # Get Time Stamp as String
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate a Unique Identifier
        unique_id = str(uuid.uuid4())[:8]

        # Combine Elements to Create the Filename
        filename = f"{base_name}_{timestamp}_{unique_id}.pdf"

        return filename

    def convert_html_to_pdf(self, source_html, output_filename):
        """
        Convert Passed HTML to PDF File
        :param source_html: str
        :param output_filename: str
        :return: None
        :state: Stable
        """

        try:
            # Prepend the MEDIA_ROOT directory to the output filename
            output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', output_filename)
            print(output_path)

            # Open Output File for Writing (Truncated Binary)
            with open(output_path, "wb") as output_file:
                # Convert HTML to PDF
                pisa_status = pisa.CreatePDF(
                    source_html,
                    dest=output_file,
                    debug=True,
                    link_callback=self.link_callback,
                )

            # Return True on Success and False on Errors
            if pisa_status.err:
                logger.exception(pisa_status.err)

            return pisa_status.err

        except FileNotFoundError:
            self.error_message = "Error: The specified file path does not exist."
            logger.exception(self.error_message)
            return False
        except PermissionError:
            self.error_message = "Error: Permission denied when trying to open the file."
            logger.exception(self.error_message)
            return False
        except IsADirectoryError:
            self.error_message = "Error: The specified path is a directory, not a file."
            logger.exception(self.error_message)
            return False
        except OSError as e:
            self.error_message = f"OS error: {e}"
            logger.exception(self.error_message)
            return False
        except ValueError:
            self.error_message = "Error: An invalid mode was passed to the open function."
            logger.exception(self.error_message)
            return False
        except TypeError:
            self.error_message = "Error: The source_html should be a string or a readable object."
            logger.exception(self.error_message)
            return False
        except Exception as e:
            self.error_message = f"An unexpected error occurred: {e}"
            logger.exception(self.error_message)
            return False

    @staticmethod
    def link_callback(uri, rel):
        """Resolve static and media asset paths for xhtml2pdf."""

        parsed = urlparse(uri)
        path = parsed.path if parsed.scheme else uri

        if path.startswith(django_settings.STATIC_URL):
            static_path = path[len(django_settings.STATIC_URL):]
            result = finders.find(static_path)
            if isinstance(result, (list, tuple)):
                return result[0]
            if result:
                return result

        if path.startswith(django_settings.MEDIA_URL):
            media_path = path[len(django_settings.MEDIA_URL):]
            return os.path.join(django_settings.MEDIA_ROOT, media_path)

        if os.path.exists(path):
            return path

        return uri

    def create_pdf_report(self, html_content):
        """
        Create PDF Report from HTML Content
        :param html_content: str
        :return: Result: boolean Output Filename: str
        :state: Stable
        """

        # Output PDF File Name
        output_pdf_filename = self.generate_unique_filename()

        # Convert the combined HTML content to a single PDF
        result = self.convert_html_to_pdf(html_content, output_pdf_filename)

        if result == 0:                             # === If No Error ===
            return True, output_pdf_filename
        else:
            logger.exception(result)
            return False, None

    @staticmethod
    def convert_and_resize_pdf_to_images(pdf_path, output_directory, desired_width, desired_height):
        """
        Converts the first three pages of a PDF to images and resizes them
        :param pdf_path: str : Path to the PDF file
        :param output_directory: str : Directory to save the images
        :param desired_width: int : Desired width of the resized images
        :param desired_height: int : Desired height of the resized images
        :return: None
        :state: Stable
        """

        # Convert pages to images
        images_cover = convert_from_path(pdf_path, first_page=1, last_page=1)
        images_summary = convert_from_path(pdf_path, first_page=2, last_page=2)
        images_calculation = convert_from_path(pdf_path, first_page=3, last_page=3)

        # Save original images
        images_cover[0].save(os.path.join(output_directory, 'image_cover.png'), 'PNG')
        images_summary[0].save(os.path.join(output_directory, 'images_summary.png'), 'PNG')
        images_calculation[0].save(os.path.join(output_directory, 'images_calculation.png'), 'PNG')

        # Function to resize and save image
        def resize_and_save(image, output_path):
            resized_image = image.resize((desired_width, desired_height), Image.Resampling.BICUBIC)
            resized_image.save(output_path, 'PNG')

        # Resize and save images
        resize_and_save(images_cover[0], os.path.join(output_directory, 'resized_image_cover.png'))
        resize_and_save(images_summary[0], os.path.join(output_directory, 'resized_image_summary.png'))
        resize_and_save(images_calculation[0], os.path.join(output_directory, 'resized_images_calculation.png'))
