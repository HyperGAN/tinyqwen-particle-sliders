"""Lightweight shared-command admission; planning does not import Torch or models."""

TRAINING_PROFILE = dict(schema='particle-slider-profile-v1', name='tinyqwen-cpu-fixture',
    product='tinyqwen-particle-sliders', config_kind='session', status='fixture',
    interface='response', backend='tinyqwen-shared-preview', runtime={},
    capabilities=dict(resume=True, periodic_checkpoint=True, check=True),
    default_checkpoint_every=2,
    qualification='Random width 16/32 CPU fixtures only; native width 1024 blocked')
