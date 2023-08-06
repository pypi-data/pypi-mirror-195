import logging
import os
import random
from functools import partial

import numpy as np
import tensorflow as tf
from PIL import Image

from .classifier import Classifier
from .classifier_wrapper import Wrapper

logger = logging.getLogger(__name__)


class Train(Wrapper):
    """Train. Trainer class"""

    def __init__(
        self,
        datas: dict,
        model_type: str,
        image_size: int,
        weight: str = None,
        mod: str = "new",
    ) -> None:
        """__init__.

        :param datas: {label:[image]}
        :type datas: dict
        :param model_type:
        :type model_type: str
        :param image_size:
        :type image_size: int
        :param weight:
        :type weight: str
        :param mod:
        :type mod: str
        :rtype: None
        """
        num_class = self.count_classes(datas)
        Wrapper.__init__(
            self,
            weight=weight,
            model_type=model_type,
            image_size=image_size,
            model_mod=mod,
            num_class=num_class,
        )

        self.datas = datas
        self.len_test_set = 0
        self.len_train_set = 0
        self.get_model_train()

    def get_model_train(self) -> object:
        """get_model_train. get model to be trained

        :rtype: object
        """
        if self.model_mod == "new":
            # input_ = self.model.input
            # pre_process = tf.keras.layers.Rescaling(1.0 / 255)(input_)

            network = self.model.output
            network = tf.keras.layers.Dense(
                self.num_class, activation="softmax", use_bias=True
            )(network)

            model = tf.keras.Model(inputs=self.model.input, outputs=network)
            self.model = model
        return self.model

    def count_classes(self, data: dict) -> int:
        """count_classes. count number of classes

        :param data:
        :type data: dict
        :rtype: int
        """
        return len(data)

    def gen_data(self, nobatch=True, test_size: float = 0.1) -> (object, object):
        """gen_data. generate data to tensorflow format

        :param test_size:
        :type test_size: float
        :rtype: (object, object)
        """
        datas = []
        for i, label in enumerate(self.datas):
            for image in self.datas[label]:
                datas += [(image, i)]
        random.shuffle(datas)
        size = int(len(datas) * (1 - test_size))
        train_set = datas[:size]
        test_set = datas[size:]
        self.len_train_set = size
        self.len_test_set = len(test_set)
        tensor_shape = [self.image_size, self.image_size, 3]
        label_shape = [self.num_class]
        if nobatch:
            tensor_shape = [1] + tensor_shape
            label_shape = [1] + label_shape

        training_set = tf.data.Dataset.from_generator(
            partial(self.generator, datas=train_set, nobatch=nobatch),
            output_signature=(
                tf.TensorSpec(shape=tensor_shape, dtype=tf.float64),
                tf.TensorSpec(shape=label_shape, dtype=tf.int8),
            ),
        )
        testing_set = tf.data.Dataset.from_generator(
            partial(self.generator, datas=test_set, nobatch=nobatch),
            output_signature=(
                tf.TensorSpec(shape=tensor_shape, dtype=tf.float64),
                tf.TensorSpec(shape=label_shape, dtype=tf.int8),
            ),
        )
        training_set = training_set.shuffle(1, reshuffle_each_iteration=True)

        return training_set, testing_set

    def generator(self, datas: list[tuple], nobatch=True) -> (np.ndarray, str):
        """generator.

        :param datas:
        :type datas: list[tuple]
        :rtype: (np.ndarray, str)
        """
        for image, label in datas:
            labels = np.zeros(self.num_class)
            labels[label] = 1
            if nobatch:
                labels = np.expand_dims(labels, axis=0)
            yield self.norm_input(image, expand=nobatch), labels

    def train(
        self,
        steps: int = 200,
        batch_size: int = 32,
        learning_rate: float = 1e-3,
        path_chkp: str = "",
    ) -> object:
        """train.

        :param steps:
        :type steps: int
        :param batch_size:
        :type batch_size: int
        :param learning_rate:
        :type learning_rate: float
        :param path_chkp:
        :type path_chkp: str
        :rtype: object
        """
        optimizer = tf.keras.optimizers.Adam(
            learning_rate=learning_rate, weight_decay=1e-4
        )
        self.model.compile(
            loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"]
        )
        if path_chkp != "":
            if os.path.isdir(path_chkp):
                os.mkdir(path_chkp)
            checkpoint = tf.keras.callbacks.ModelCheckpoint(
                filepath=path_chkp,
                monitor="accuracy",
                verbose=1,
                save_weights_only=True,
                save_best_only=True,
                period=1,
            )
        else:
            checkpoint = None
        train_set, valid_set = self.gen_data(batch_size == 0)
        if batch_size != 0:
            train_set = train_set.batch(batch_size)
            valid_set = valid_set.batch(batch_size)

            self.model.fit(
                train_set.repeat(),
                steps_per_epoch=self.len_train_set // batch_size,
                epochs=steps,
                validation_data=valid_set.repeat(),
                validation_steps=self.len_test_set // batch_size,
                callbacks=None,
            )
        else:
            self.model.fit(
                train_set,
                epochs=steps,
                validation_data=valid_set,
                callbacks=None,
            )
        return self.model


def train(
    datas: dict,
    model_type: str = "MobileNetV2",
    image_size: int = 300,
    batch_size: int = 32,
    epochs: int = 100,
    checkpoint: str = "",
    add: bool = False,
) -> Classifier:
    """train.

    :param datas: {label:[image]}
    :type datas: dict
    :param model_type:
    :type model_type: str
    :param image_size:
    :type image_size: int
    :param checkpoint:
    :type checkpoint: str
    :param add:
    :type add: bool
    :rtype: Classifier
    """
    if checkpoint == "" and not add:
        trainer = Train(datas, model_type=model_type, image_size=image_size, mod="new")
    elif checkpoint == "" and add:
        image_size = 300
        model_type = ""
        weight = None
        trainer = Train(
            datas,
            model_type=model_type,
            weight=weight,
            image_size=image_size,
            mod="add",
        )
    else:
        image_size = 300
        model_type = ""
        weight = None
        trainer = Train(
            datas,
            model_type=model_type,
            weight=weight,
            image_size=image_size,
            mod="resume",
        )
    model = trainer.train(path_chkp=checkpoint, steps=epochs, batch_size=batch_size)
    return Classifier(
        model=model,
        model_type=model_type,
        image_size=image_size,
        preprocess=trainer.preprocess,
        decode=trainer.decode,
        num_class=trainer.num_class,
    )
