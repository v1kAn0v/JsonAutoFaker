import re
import clipboard
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


def json_faker_automata(schema_path: str, output_path: str, prefix: str, file_count: int) -> None:

    def paste() -> None:
        # Paste json schema
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "bu")))
        input_form = driver.find_elements(By.CLASS_NAME, "ace_text-input")
        input_form[0].send_keys(Keys.COMMAND + 'a')
        input_form[0].send_keys(schema)

    def generate() -> str:
        # Generate sample json text
        driver.find_element(By.CLASS_NAME, "bu").click()

        # Copy generated json text
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ace_content")))
        output_form = driver.find_elements(By.CLASS_NAME, "ace_text-input")
        output_form[1].send_keys(Keys.COMMAND + 'a')
        output_form[1].send_keys(Keys.COMMAND + 'c')
        return clipboard.paste()

    with open(schema_path, encoding="utf-8") as reader:
        data = json.load(reader)
    schema = json.dumps(data, separators=(",", ":"))

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://json-schema-faker.js.org/')
    paste()

    for num in range(file_count):
        json_text = generate()
        json_text = re.sub("(?<=19)([0-6])(?=[0-9]-)", "7", json_text)
        # Save json text into json sample file
        with open("%s/%s%s.md.json" % (output_path, prefix, str(num).zfill(4)), "w", encoding="utf-8") as writer:
            writer.write(json_text)


if __name__ == '__main__':

    json_faker_automata(schema_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/"
                                    "schemas/consolidated/consolidated_Image_single_instance_schema.json",
                        output_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/media/images",
                        prefix="image",
                        file_count=1000)

    json_faker_automata(schema_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/"
                                    "schemas/consolidated/consolidated_Telemetry_single_instance_schema.json",
                        output_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/media/telemetry",
                        prefix="telemetry",
                        file_count=1000)
    json_faker_automata(schema_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/"
                                    "schemas/consolidated/consolidated_Video_single_instance_schema.json",
                        output_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/media/video",
                        prefix="video",
                        file_count=1000)
    json_faker_automata(schema_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/"
                                    "schemas/consolidated/consolidated_SignalsComint_single_instance_schema.json",
                        output_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/media/signals",
                        prefix="signals",
                        file_count=1000)
