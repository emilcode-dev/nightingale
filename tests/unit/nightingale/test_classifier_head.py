import pytest
from nightingale.model.classifier_head import ClassifierHead
import numpy as np

@pytest.fixture
def classifier_head():
    return ClassifierHead(num_classes=10)

def test_classifier_head_forward(classifier_head):
    # Test the forward pass
    x = np.random.randn(32, 128)
    logits = classifier_head(x)
    assert logits.shape == (32, 10)
