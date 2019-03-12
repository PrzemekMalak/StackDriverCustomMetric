import time
import random
from google.cloud import monitoring_v3 as gcm


def get_client():
    client = gcm.MetricServiceClient()
    return client

def get_metric_name(metric_name):
    return 'custom.googleapis.com/' + metric_name

def get_project_name(client, project_id):
    project_name = client.project_path(project_id)
    return project_name

def create_descriptor(metric_name):
    descriptor = gcm.types.MetricDescriptor()
    descriptor.type = get_metric_name(metric_name)
    descriptor.metric_kind = (
        gcm.enums.MetricDescriptor.MetricKind.GAUGE)
    descriptor.value_type = (
        gcm.enums.MetricDescriptor.ValueType.DOUBLE)
    descriptor.description = 'This is an example of a custom metric.'
    descriptor = client.create_metric_descriptor(project_name, descriptor)
    print('Created {}.'.format(descriptor.name))
    return descriptor

def save_metric(instance_id, metric_name, value):
    series = gcm.types.TimeSeries()
    series.metric.type = get_metric_name(metric_name)
    series.resource.type = 'gce_instance'
    series.resource.labels['instance_id'] =instance_id
    series.resource.labels['zone'] = 'europe-west3-a'
    point = series.points.add()
    point.value.double_value = value
    now = time.time()
    point.interval.end_time.seconds = int(now)
    point.interval.end_time.nanos = int(
        (now - point.interval.end_time.seconds) * 10**9)
    client.create_time_series(project_name, [series])

metric_name = 'my_test_metric'
client = get_client()
project_name = get_project_name(client, 'pocofin')
descriptor = create_descriptor(metric_name)

for idx in range(0,20):
    save_metric('cloud_shell', metric_name, idx)
    time.sleep(60)