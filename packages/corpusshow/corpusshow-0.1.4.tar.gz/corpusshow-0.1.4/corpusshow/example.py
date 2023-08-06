from corpus_cluster import CorpusCluster


if __name__ == "__main__":
    csv_file_path = r"C:\Users\parkm\Desktop\github\fine-tuned-korean-BERT-news-article-classifier\data\test_set2.csv"
    sentence_transformer_model_name = 'paraphrase-xlm-r-multilingual-v1'
    target_col = 'cleanBody'
    num_cluster = 8
    cc = CorpusCluster(csv_file_path, sentence_transformer_model_name, target_col, num_cluster)
    cc.quick_cluster_show('tsne2d', 'test.png')