"""Switch platform for Hughes Power Watchdog integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONNECTION_CHECK_INTERVAL, DOMAIN, SWITCH_MONITORING
from .coordinator import HughesPowerWatchdogCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Hughes Power Watchdog switches."""
    coordinator: HughesPowerWatchdogCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    async_add_entities([HughesPowerWatchdogMonitoringSwitch(coordinator)])


class HughesPowerWatchdogMonitoringSwitch(
    CoordinatorEntity[HughesPowerWatchdogCoordinator], SwitchEntity
):
    """Monitoring switch for Hughes Power Watchdog."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:connection"

    def __init__(self, coordinator: HughesPowerWatchdogCoordinator) -> None:
        """Initialize the monitoring switch."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{SWITCH_MONITORING}"
        self._attr_name = "Monitoring"
        self._attr_device_info = coordinator.device_info
        self._attr_is_on = coordinator.monitoring_enabled

    @property
    def is_on(self) -> bool:
        """Return true if monitoring is enabled."""
        return self.coordinator.monitoring_enabled

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on - enable monitoring."""
        from datetime import timedelta

        # Resume connection watchdog
        self.coordinator.update_interval = timedelta(seconds=CONNECTION_CHECK_INTERVAL)

        # Restart background tasks and reconnect
        self.coordinator.start_monitoring()

        await self.coordinator.async_refresh()
        self.async_write_ha_state()
        _LOGGER.debug("Monitoring enabled for %s", self.coordinator.address)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off - disable monitoring."""
        # Stop connection watchdog
        self.coordinator.update_interval = None

        # Unsubscribe, disconnect, and cleanup
        await self.coordinator.async_disconnect()

        self.async_write_ha_state()
        _LOGGER.debug("Monitoring disabled for %s", self.coordinator.address)
