from huggingface_hub import snapshot_download

snapshot_download(
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    local_dir="backend/model/roberta",
    local_dir_use_symlinks=False
)
print("Model downloaded to backend/model/roberta")
