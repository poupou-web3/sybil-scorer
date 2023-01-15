import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.metrics import silhouette_samples
import numpy as np
import pandas as pd
import seaborn as sns
import os
sns.set_theme()

def scatter_plot_2d(data_2d, color_col, title):
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=color_col, cmap="jet", alpha=0.4)
    plt.title(title)
    plt.xticks(())
    plt.yticks(())
    plt.colorbar()
    plt.show()
    
def plot_silhouette_score(np_dataset, kmeans_results, kmeans_silhouette, min_cluster, max_cluster):
    for n_cluster in range (min_cluster, max_cluster+1):
        plot_silhouette_score_cluster(np_dataset, kmeans_results, kmeans_silhouette, min_cluster, n_cluster)
    

def plot_silhouette_score_cluster(np_dataset, kmeans_results, kmeans_silhouette, min_cluster, n_cluster):
    fig, ax1 = plt.subplots()
    fig.set_size_inches(10, 7)

    # The subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.3, 1]
    ax1.set_xlim([-0.3, 1])  # type: ignore
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(np_dataset) + (n_cluster + 1) * 10])  # type: ignore

    # labels of the kth cluster
    cluster_labels = kmeans_results[n_cluster-min_cluster].labels_

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = kmeans_silhouette[n_cluster-min_cluster]
    print("For n_clusters =", n_cluster,
            "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(np_dataset, labels=cluster_labels, metric='euclidean')

    y_lower = 10

    # sort by order of occurences
    clusters = np.unique(kmeans_results[n_cluster-min_cluster].labels_)
    occurences = [np.count_nonzero(cluster_labels == i) for i in clusters]
    df_occurences = pd.DataFrame(occurences)
    df_occurences = df_occurences.set_axis(['occurences'], axis=1, copy=False)
    df_occurences.sort_values(by=['occurences'], ascending=False, inplace=True)
    df_occurences['percentage'] = df_occurences['occurences'] / np_dataset.shape[0] * 100
    print(df_occurences)

    for i in df_occurences.index:

        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()


        size_cluster_i = ith_cluster_silhouette_values.shape[0]

        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_cluster)  # type: ignore
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                            0, ith_cluster_silhouette_values,
                            facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, 'k=' + str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                    "with n_clusters = %d" % n_cluster),
                    fontsize=14, fontweight='bold')
    plt.show()

def save_hist(df, path_to_save, cluster_col_name=None, debug=False):
    if cluster_col_name == None:
        cols = df.drop(columns=[cluster_col_name]).columns
    else:
        cols = df.columns
        
    i = 0
    for i_col in cols:
        if i_col not in ["timeStamp__variance_larger_than_standard_deviation", "value__abs_energy"]: # cause bug out of memory!
            if debug:
                print(str(i) + " " + i_col)
                i += 1
                
            if cluster_col_name == None:
                sns_plot = sns.histplot(df, x=i_col)
            else:
                n_cluster = len(df[cluster_col_name].unique())
                sns_plot = sns.histplot(df, x=i_col, hue=cluster_col_name, palette=sns.color_palette('bright', n_colors=n_cluster))
            fig_name = i_col + ".png"
            fig = sns_plot.get_figure()

            if not os.path.exists(path_to_save):
                os.makedirs(path_to_save)

            fig.savefig(os.path.join(path_to_save, fig_name))
            fig.clf() 
            plt.close()
    

def plot_PCA(reduced_data, kmeans):
    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .01     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation="nearest",
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired, aspect="auto", origin="lower")  # type: ignore

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=169, linewidths=3,  # type: ignore
                color="w", zorder=10)
    plt.title("K-means clustering on squore (PCA-reduced data)\n"
              "Centroids are marked with white cross")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()    


def plot_kmean_inertia(kmeans_inertia, min_cluster, max_cluster):
    range_n_clusters = np.linspace(min_cluster,max_cluster,max_cluster-min_cluster+1)
    ax = sns.lineplot(x=range_n_clusters, y=kmeans_inertia)
    ax.set_title('Inertia with kmean')
    ax.set_ylabel('inertia')
    ax.set_xlabel('# clusters')


def plot_kmean_silhouette_score(kmeans_silhouette, min_cluster, max_cluster):
    range_n_clusters = np.linspace(min_cluster,max_cluster,max_cluster-min_cluster+1)
    ax = sns.lineplot(x=range_n_clusters, y=kmeans_silhouette)
    ax.set_title('Mean silhouette score')
    ax.set_ylabel('Silhouette score')
    ax.set_xlabel('# clusters')


def plot_silhouette_tsne_save_hist(df, kmeans_results, kmeans_silhouette, min_cluster, max_cluster, X_embedded, absolute_path, tx_chain, save=False):
    np_dataset = df.values
    for n_cluster in range (min_cluster, max_cluster+1):
        plot_silhouette_score_cluster(np_dataset, kmeans_results, kmeans_silhouette, min_cluster, n_cluster)

        df_occurences, cluster_labels = get_df_occurences(np_dataset, kmeans_results, n_cluster, min_cluster)
        print(df_occurences)

        scatter_plot_2d(X_embedded, cluster_labels, 't_sne reduction k_mean clusters k={} outlier removed'.format(n_cluster))

        df["cluster"] = cluster_labels
        
        for cluster in (df_occurences.index.values):
            df_small_cluster = df[df['cluster'] == cluster]
            print("k={}, cluster = {}".format(n_cluster, cluster))
            print(df_small_cluster.sample(n=(min(4, df_small_cluster.shape[0]))).index)

        if save:
            path_charts = os.path.join(absolute_path, "charts_kmean")
            path_charts = os.path.join(path_charts, tx_chain)
            path_charts = os.path.join(path_charts, "k={}".format(n_cluster))
            
            # save_hist(df.iloc[:, -10:], path_charts, cluster_col_name="cluster", debug=False)
            save_hist(df, path_charts, cluster_col_name="cluster", debug=True)
        


def save_hist_clusters(df, kmeans_results, min_cluster, max_cluster ,absolute_path, tx_chain, debug=False):
    np_dataset = df.values
    for n_cluster in range (min_cluster, max_cluster+1):

        df_occurences, cluster_labels = get_df_occurences(np_dataset, kmeans_results, n_cluster, min_cluster)

        path_charts = os.path.join(absolute_path, "charts_kmean")
        path_charts = os.path.join(path_charts, tx_chain)
        path_charts = os.path.join(path_charts, "k={}".format(n_cluster))

        df["cluster"] = cluster_labels
        # save_hist(df.iloc[:, -10:], path_charts, cluster_col_name="cluster", debug=False)
        save_hist(df, path_charts, cluster_col_name="cluster", debug=False)


def get_df_occurences(np_data, kmeans_results, n_clusters, min_cluster):
    cluster_labels = kmeans_results[n_clusters-min_cluster].labels_
    clusters = np.unique(kmeans_results[n_clusters-min_cluster].labels_)
    occurences = [np.count_nonzero(cluster_labels == i) for i in clusters]
    df_occurences = pd.DataFrame(occurences)
    df_occurences = df_occurences.set_axis(['occurences'], axis=1, copy=False)
    df_occurences.sort_values(by=['occurences'], ascending=False, inplace=True)
    df_occurences['percentage'] = df_occurences['occurences'] / np_data.shape[0] * 100
    
    return df_occurences, cluster_labels

