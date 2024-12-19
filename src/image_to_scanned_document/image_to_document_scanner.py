import os
import cv2
import numpy as np
import math
from PIL import Image as PILImage


class ImageToPdfScanner:
    def __init__(self, input_image_path, output_pdf_path):
        self.input_image_path = input_image_path
        self.output_pdf_path = output_pdf_path

    def load_image(self):
        image = cv2.imread(self.input_image_path, cv2.IMREAD_COLOR)
        return image

    def resize_image(self, image, width=800, height=600):
        return cv2.resize(image, (width, height))

    def preprocess_image(self, image):

        resized_original = self.resize_image(image)

        # Korak 1: Konvertiraj u grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_grayscale = self.resize_image(grayscale_image)


        # Korak 2: Primjerni Gaussian Blur
        blurred_image = cv2.GaussianBlur(grayscale_image, (99, 99), 0)

        resized_blurred = self.resize_image(blurred_image)

        # Korak 3: Pretvori u binarnu sliku
        _, binary_image = cv2.threshold(blurred_image, 90, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        resized_binary = self.resize_image(binary_image)


        # Korak 4: Pronađi obrise
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            raise ValueError("Nisu pronađeni obrisi (oblici) na slici.")


        contour_image_bw = np.zeros_like(binary_image)
        cv2.drawContours(contour_image_bw, contours, -1, (255), 1)
        resized_contour_bw = self.resize_image(contour_image_bw)


        # Korak 5: Pronađi najveći obris (oblik) i aproksimiraj njegove kuteve
        largest_contour = max(contours, key=cv2.contourArea)
        epsilon = 0.1 * cv2.arcLength(largest_contour, True)
        approx_polygon = cv2.approxPolyDP(largest_contour, epsilon, True)

        if len(approx_polygon) != 4:
            raise ValueError("Nije moguće detektirati obris sa 4 kuta.")

        point1 = approx_polygon[0][0]
        point2 = approx_polygon[1][0]
        point3 = approx_polygon[2][0]
        point4 = approx_polygon[3][0]

        approx_polygon_image = image.copy()
        cv2.polylines(approx_polygon_image, [approx_polygon], isClosed=True, color=(0, 255, 0), thickness=3)
        resized_approx_image = self.resize_image(approx_polygon_image)


        # Korak 7: Izračunaj stranice i odredi orijentaciju
        edge1 = math.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))
        edge2 = math.sqrt(((point2[0] - point3[0]) ** 2) + ((point2[1] - point3[1]) ** 2))
        edge3 = math.sqrt(((point3[0] - point4[0]) ** 2) + ((point3[1] - point4[1]) ** 2))
        edge4 = math.sqrt(((point4[0] - point1[0]) ** 2) + ((point4[1] - point1[1]) ** 2))

        side_1 = round(min(edge1, edge3))
        side_2 = round(min(edge2, edge4))

        if side_1 > side_2:
            height = side_1
            width = side_2
            ordered_corners = [point1, point4, point2, point3]
        else:
            height = side_2
            width = side_1
            ordered_corners = [point2, point1, point3, point4]

        # Korak 8: Napravi transformaciju
        source_points = np.float32(ordered_corners)
        destination_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

        transformed_image = cv2.warpPerspective(image, perspective_matrix, (width, height))

        resized_transformed = self.resize_image(transformed_image)

        # Kako bi se mogli prikazati međukoraci zajedno, moramo konvertirati sve slike da imaju isti broj dimenzija
        resized_grayscale = cv2.cvtColor(resized_grayscale, cv2.COLOR_GRAY2BGR)
        resized_blurred = cv2.cvtColor(resized_blurred, cv2.COLOR_GRAY2BGR)
        resized_binary = cv2.cvtColor(resized_binary, cv2.COLOR_GRAY2BGR)
        resized_contour_bw = cv2.cvtColor(resized_contour_bw, cv2.COLOR_GRAY2BGR)

        concatenated_images = np.concatenate(
            (resized_original,
             resized_grayscale,
             resized_blurred,
             resized_binary,
             resized_contour_bw,
             resized_approx_image,
             resized_transformed), axis=0)

        concatenated_images_rgb = cv2.cvtColor(concatenated_images, cv2.COLOR_BGR2RGB)
        output_directory = os.path.dirname(self.output_pdf_path)
        steps_pdf_path = os.path.join(output_directory, "koraci.pdf")

        pil_image = PILImage.fromarray(concatenated_images_rgb)
        pil_image.save(steps_pdf_path, "PDF")

        return transformed_image

    def save_image_as_pdf(self, transformed_image):
        pil_image = PILImage.fromarray(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))
        pil_image.save(self.output_pdf_path, "PDF")

    def process_and_save(self):
        image = self.load_image()
        transformed_image = self.preprocess_image(image)
        self.save_image_as_pdf(transformed_image)