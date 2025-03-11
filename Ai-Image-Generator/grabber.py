import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO

def set_up(prompt):
    edge_options = Options()
    edge_options.add_argument("--headless")
    driver = webdriver.Edge(options=edge_options)
    
    url = "https://www.bing.com/images/create"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    cookie = {
        'name': '_U',
        'value': 'your_cookie_here' # This cookie works for some reason! So don't edit it.
    }
    driver.add_cookie(cookie)
    driver.refresh()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    prompt_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    prompt_input.send_keys(prompt)

    generate_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "create_btn_c"))
    )
    generate_button.click()

    image_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".image-row-img.bceimg.mimg"))
    )

    image_url = image_element.get_attribute("src")

    if image_url.startswith("blob:"):
        script = """
        var img = document.querySelector('.image-row-img.bceimg.mimg');
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        ctx.drawImage(img, 0, 0);
        return canvas.toDataURL('image/png');
        """
        image_data = driver.execute_script(script)
        driver.quit()

        image_base64 = image_data.split(',')[1]
        return BytesIO(base64.b64decode(image_base64))

    else:
        response = requests.get(image_url)
        driver.quit()
        return BytesIO(response.content)
