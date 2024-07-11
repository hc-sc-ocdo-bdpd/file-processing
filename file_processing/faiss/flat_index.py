from file_processing.faiss.faiss_strategy import FAISSStrategy

class FlatIndex(FAISSStrategy):
    def __init__(self) -> None:
        super().__init__()
    
    def _create_index(self):
        pass