import pytest
from app.models import Device

def describe_device():
  def test_device_creation():
      device = Device.create_with({
          'name': 'Test Device',
          'hash': 'abcd',
      })

      device = Device.find_by(hash='abcd')

      assert device.name == 'Test Device'
