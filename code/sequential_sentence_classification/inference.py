from allennlp.common.util import JsonDict
from allennlp.predictors.predictor import Predictor


@Predictor.register('SeqClassificationInference')
class SeqClassificationInference(Predictor):
    """
    Predictor for the abstruct model
    """
    def predict_json(self, json_dict: JsonDict) -> JsonDict:
        print("#############Only inference###########")
        print("************************P*************")
        pred_labels = []
        sentences = json_dict['sentences']
        for sentences_loop, _, _, _ in self._dataset_reader.enforce_max_sent_per_example(sentences):
            instance = self._dataset_reader.text_to_instance(sentences=sentences_loop)
            output = self._model.forward_on_instance(instance)
            idx = output['action_probs'].argmax(axis=1).tolist()
            labels = [self._model.vocab.get_token_from_index(i, namespace='labels') for i in idx]
            pred_labels.extend(labels)
        preds = list(zip(sentences, pred_labels))
        print("xxxx", preds)
        return preds
