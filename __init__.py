"""Camera platform for Folder Image Slideshow."""

from __future__ import annotations

import os
import random

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_FILE_PATH
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the Folder Image Slideshow Camera."""
    directory = hass.data[DOMAIN][entry.entry_id]["directory"]
    camera = SlideshowCamera(directory)
    async_add_entities([camera])


class SlideshowCamera(Camera):
    """Representation of a Folder Image Slideshow Camera."""

    def __init__(self, directory: str) -> None:
        """Initialize the camera."""
        super().__init__()
        self.directory = directory
        self._last_image = None
        self.update_interval = timedelta(minutes=1)
        self._update_image()
        async_track_time_interval(self.hass, self._update_image, self.update_interval)

    def camera_image(self):
        """Return the image for the camera."""
        return self._last_image

    def _update_image(self, now=None):
        """Update the image with a random image from the directory."""
        files = [
            os.path.join(self.directory, f)
            for f in os.listdir(self.directory)
            if os.path.isfile(os.path.join(self.directory, f))
        ]
        if files:
            image_path = random.choice(files)
            with open(image_path, "rb") as img_file:
                self._last_image = img_file.read()
            self.async_write_ha_state()
