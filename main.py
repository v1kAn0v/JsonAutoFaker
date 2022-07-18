import time
import clipboard
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json
from selenium.webdriver.common.keys import Keys


def test_selenium_google_drive_service():
    with open("/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/schemas/"
              "consolidated/consolidated_Image_single_instance_schema.json", encoding="utf-8") as f:
        data = json.load(f)

    driver = webdriver.Chrome('/Users/sergey/Downloads/chromedriver')
    driver.get('https://json-schema-faker.js.org/')
    schema = json.dumps(data, separators=(",", ":"))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "bu")))
    input_form = driver.find_elements(By.CLASS_NAME, "ace_text-input")
    input_form[0].send_keys(schema)

    driver.find_element(By.CLASS_NAME, "bu").click()

    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ace_content")))
    output_form = driver.find_elements(By.CLASS_NAME, "ace_text-input")
    output_form[1].send_keys(Keys.COMMAND + 'a')
    output_form[1].send_keys(Keys.COMMAND + 'c')
    text = clipboard.paste()
    with open("/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/"
              "tests/media/happy/image0000.md.json", "w", encoding="utf-8") as f:
        f.write(text)
    time.sleep(300)


def json_faker_automata(schema_path: str, output_path: str, prefix: str, file_count: int) -> None:

    def generate() -> str:
        with open(schema_path, encoding="utf-8") as reader:
            data = json.load(reader)

        driver = webdriver.Chrome('/Users/sergey/Downloads/chromedriver')
        driver.get('https://json-schema-faker.js.org/')
        schema = json.dumps(data, separators=(",", ":"))

        # Paste json schema
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "bu")))
        input_form = driver.find_elements(By.CLASS_NAME, "ace_text-input")
        input_form[0].send_keys(Keys.COMMAND + 'a')
        input_form[0].send_keys(schema)

        # Generate sample json text
        driver.find_element(By.CLASS_NAME, "bu").click()

        # Copy generated json text
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ace_content")))
        output_form = driver.find_elements(By.CLASS_NAME, "ace_text-input")
        output_form[1].send_keys(Keys.COMMAND + 'a')
        output_form[1].send_keys(Keys.COMMAND + 'c')
        return clipboard.paste()

    for num in range(file_count):
        json_text = generate()

        # Save json text into json sample file
        with open("%s/%s%s.md.json" % (output_path, prefix, str(num).zfill(4)), "w", encoding="utf-8") as writer:
            writer.write(json_text)


if __name__ == '__main__':
    json_faker_automata(schema_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/"
                                    "schemas/consolidated/consolidated_Image_single_instance_schema.json",
                        output_path="/Users/sergey/PycharmProjects/DAITA/DataCatalogAPI/tests/media/images",
                        prefix="image",
                        file_count=2)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
