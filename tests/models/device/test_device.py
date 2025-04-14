from app.models import Device

def describe_device():
  def describe_when_hash_is_unique():
    def it_creates_an_device():
        device = Device.create_with({
            'name': 'Test Device',
            'hash': 'abcd',
        })

        device = Device.find_by(hash='abcd')

        assert device.name == 'Test Device'

  def describe_when_hash_is_not_unique():
    def it_does_not_create_an_device():
        Device.create_with({
            'name': 'Test Device',
            'hash': 'abcd',
        })

        try:
            Device.create_with({
                'name': 'Another Test Device',
                'hash': 'abcd',
            })
        except Exception as e:
           pass

        assert Device.select().count() == 1

  def describe_when_name_is_not_unique():
    def it_creates_an_device():
        Device.create_with({
            'name': 'Test Device',
            'hash': 'abcd',
        })

        try:
            Device.create_with({
                'name': 'Test Device',
                'hash': 'abce',
            })
        except Exception as e:
           pass

        assert Device.select().count() == 2
