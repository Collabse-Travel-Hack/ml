from abc import ABC, abstractmethod
import torch
from transformers import AutoTokenizer, AutoModel


class EmbedderABC(ABC):
    @abstractmethod
    def predict(self, text):
        pass


class RuBERTEmbedder(EmbedderABC):
    def __init__(self, device=None, max_length=512):
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)

        if not torch.cuda.is_available():
            print('CUDA is not available. Using CPU')

        self.tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
        self.model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        self.max_length = max_length

    @torch.no_grad()
    def predict(self, texts):
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, max_length=self.max_length,
                                       return_tensors='pt').to(self.device)
        model_output = self.model(**encoded_input)
        embeddings = model_output.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings
