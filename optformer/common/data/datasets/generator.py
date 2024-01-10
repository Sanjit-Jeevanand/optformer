# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Dataset creation from a generator."""

from typing import Iterator, TypeVar

import attrs
from optformer.common.data import featurizers
from optformer.common.data.datasets import base
import tensorflow as tf

_S = TypeVar('_S')


@attrs.define
class GeneratorDatasetFn(base.DatasetFn[_S]):
  """Dataset will load from a featurized generator."""

  featurizer: featurizers.Featurizer[_S] = attrs.field(init=True, kw_only=True)

  def __call__(self, source: Iterator[_S]) -> tf.data.Dataset:
    def _generator():
      for obj in source:
        yield self.featurizer.to_features(obj)

    return tf.data.Dataset.from_generator(
        _generator,
        output_types=self.featurizer.output_types,
        output_shapes=self.featurizer.output_shapes,
    )
