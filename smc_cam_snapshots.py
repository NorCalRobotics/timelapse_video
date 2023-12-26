# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchWindowException,\
    TimeoutException, JavascriptException
from selenium.webdriver.common.by import By
from typing import Callable
import time
import glob
import cv2
import os

# settings:
# The SMC Camera's snapshot saving settings should be set to this path
img_cap_dir = 'C:/Users/Public/Pictures'


def set_img_cap_dir(dirname: str):
    global img_cap_dir
    img_cap_dir = dirname


class SMCIface:
    def __init__(self, hostname: str):
        ie_options = webdriver.IeOptions()
        ie_options.attach_to_edge_chrome = True

        self.driver = webdriver.Ie(options=ie_options)
        self.driver.get('http://' + hostname)
        self.control_frame = self.driver.find_elements(By.TAG_NAME, 'iframe')[0]
        self.driver.switch_to.frame(self.control_frame)
        self.imgSnapshot = self.driver.find_element(By.ID, "imgSnapshot")

        # Tracking JPEG files in the snapshots directory, so that new ones are noted after triggering a snapshot
        self.last_jpg_file_list = self.get_snapshots_dir_jpg_filename_list()

        self.browser_closed_callback: Callable[[], None] = None
        self.snapshot_log_callback: Callable[[str], None] = None
        self.delete_jpegs : bool = True

    def __del__(self):
        self.driver.quit()

    def set_browser_closed_callback(self, cb: Callable[[], None]):
        self.browser_closed_callback = cb

    def set_snapshot_log_callback(self, cb: Callable[[str], None]):
        self.snapshot_log_callback = cb

    def get_snapshots_dir_jpg_filename_list(self):
        jpg_filename_list = glob.glob(img_cap_dir + '/*.jpg')
        if jpg_filename_list is None:
            jpg_filename_list = []
        return jpg_filename_list

    def get_snapshot_img(self):
        try:
            self.driver.execute_script("snapshot()")
        except UnexpectedAlertPresentException:
            return None
        except TimeoutException:
            return None
        except JavascriptException:
            return None
        except NoSuchWindowException:
            if self.browser_closed_callback is not None:
                self.browser_closed_callback()

        time.sleep(3.5)

        # Look for new JPEG files in the snapshots directory
        jpg_file_list = self.get_snapshots_dir_jpg_filename_list()

        # Prevent uninitialized return values
        img = None

        # Read the new snapshot image(s)
        for jpg_filename in jpg_file_list:
            if jpg_filename not in self.last_jpg_file_list:
                if self.snapshot_log_callback is not None:
                    self.snapshot_log_callback(jpg_filename)
                img = cv2.imread(jpg_filename)

                # Remove the file after it's read into memory
                if self.delete_jpegs:
                    try:
                        os.remove(jpg_filename)
                    except PermissionError:
                        pass

        # Update the list of JPEG files in the snapshots directory
        self.last_jpg_file_list = jpg_file_list

        # Return the snapshot image that's in memory
        return img
