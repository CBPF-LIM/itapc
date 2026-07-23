from app.models import Experiment

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 302

def test_experiment(client):
    experiment = Experiment.create_with({
        'name': 'test_experiment',
        'header': 'test_header'
    })
    count = Experiment.all().count()
    assert count == 1

def test_another_experiment(client):
    experiment = Experiment.create_with({
        'name': 'test_experiment2',
        'header': 'test_header2'
    })
    count = Experiment.all().count()
