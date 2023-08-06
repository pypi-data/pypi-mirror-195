from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import pandas as pd
import quickshow as qs


class CorpusCluster:
    def __init__(self, csv_file_path, sentence_transformer_model_name, target_col, num_cluster) -> None:
        self.df = pd.read_csv(csv_file_path)
        self.embedder =  SentenceTransformer(sentence_transformer_model_name)
        self.num_cluster = num_cluster
        self.sentence_transformer_model_name = sentence_transformer_model_name
        self.target_col = target_col


    @staticmethod
    def get_corpus_cluster_df(corpus: list, sentence_transformer_model_name: str, num_cluster: int) -> list:
        embedder = SentenceTransformer(sentence_transformer_model_name)
        corpus_embeddings = embedder.encode(corpus)
        k_means_model = KMeans(n_clusters=num_cluster)
        k_means_model.fit(corpus_embeddings)
        cluster_assignment = k_means_model.labels_
        clustered_corpus = [[] for i in range(num_cluster)]
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            clustered_corpus[cluster_id].append(corpus[sentence_id])
        clustered_list = [[str(i)+'cluster'+x for x in clustered_corpus[i]] for i in range(num_cluster)]

        return sum(clustered_list, [])


    def get_df_cluster(self) -> pd.DataFrame:
        self.df.reset_index()
        self.df[self.target_col] = [f'{i}index{b}' for i, b in enumerate(self.df[self.target_col])] 
        corpus = self.df[self.target_col].to_list()
        clusted_corpus = self.get_corpus_cluster_df(corpus, self.sentence_transformer_model_name, self.num_cluster)
        
        df_cluster = pd.DataFrame(clusted_corpus, columns=[self.target_col])
        df_cluster['cluster'] = [int(x.split('cluster')[0]) for x in df_cluster[self.target_col]]
        df_cluster[self.target_col] = [x.split('cluster')[1] for x in df_cluster[self.target_col]]
        df_cluster['index'] = [int(x.split('index')[0]) for x in df_cluster[self.target_col]]
        df_cluster[self.target_col] = [x.split('index')[1] for x in df_cluster[self.target_col]]
        df_cluster.drop([self.target_col], axis = 1, inplace=True)

        self.df['index'] = [int(x.split('index')[0]) for x in self.df[self.target_col]]
        self.df[self.target_col] = [x.split('index')[1] for x in self.df[self.target_col]]
        self.df = self.df.join(df_cluster.set_index('index'), on='index')

        return self.df
    

    def quick_cluster_show(self, vis_type, save_plot_path) -> pd.DataFrame:
        if 'cluster' not in self.df:
            self.df = self.get_df_cluster()
        if 'embedded_sentence' not in self.df.columns:
            self.df['embedded_sentence'] = [self.embedder.encode(str(x)) for x in self.df[self.target_col]]
            
        if vis_type == 'tsne2d':
            return_df = qs.vis_tsne2d(self.df, 'embedded_sentence', 'cluster', True, save_plot_path)
        elif vis_type == 'tsne3d':
            return_df  = qs.vis_tsne3d(self.df, 'embedded_sentence', 'cluster', True, save_plot_path)
        elif vis_type == 'pca2d':
            return_df = qs.vis_pca(self.df, 'embedded_sentence', 'cluster', 2, True, save_plot_path)
        elif vis_type == 'pca3d':
            return_df = qs.vis_pca(self.df, 'embedded_sentence', 'cluster', 3, True, save_plot_path)
        
        return return_df


    def quick_corpus_show(self, true_label_col: str, vis_type: str, save_plot_path: str) -> None:
        if 'embedded_sentence' not in self.df.columns:
            self.df['embedded_sentence'] = [self.embedder.encode(str(x)) for x in self.df[self.target_col]]

        if vis_type == 'tsne2d':
            return_df = qs.vis_tsne2d(self.df, 'embedded_sentence', true_label_col, True, save_plot_path)
        elif vis_type == 'tsne3d':
            return_df  = qs.vis_tsne3d(self.df, 'embedded_sentence', true_label_col, True, save_plot_path)
        elif vis_type == 'pca2d':
            return_df = qs.vis_pca(self.df, 'embedded_sentence', true_label_col, 2, True, save_plot_path)
        elif vis_type == 'pca3d':
            return_df = qs.vis_pca(self.df, 'embedded_sentence', true_label_col, 3, True, save_plot_path)
        
        return return_df


if __name__ == "__main__":
    csv_file_path = r"C:\Users\parkm\Desktop\github\fine-tuned-korean-BERT-news-article-classifier\data\test_set2.csv"
    sentence_transformer_model_name = 'paraphrase-xlm-r-multilingual-v1'
    target_col = 'cleanBody'
    num_cluster = 8
    cc = CorpusCluster(csv_file_path, sentence_transformer_model_name, target_col, num_cluster)
    cc.quick_cluster_show('tsne2d', 'test.png')