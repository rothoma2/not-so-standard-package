from typing import Dict 
from features.features_model import Features, PackageFeartures
from features.features import SnippetStats

def make_features(package_id:str, package_name:str, file_name:str, file:str):

    snippet_stats = SnippetStats()

    snippet_stats.set_snippet(file)

    snippet_features = Features(
        package_id=package_id,
        package_name=package_name,
        file_name=file_name,
        # quantitative features
        shanon_entropy__file=snippet_stats.shannon_entropy__file(), # entropy of the entire file
        # the quantities below are based on statistics of each line in the file
        shanon_entropy__number_outliers= snippet_stats.shannon_entropy__file(),
        shanon_entropy__mean= snippet_stats.shannon_entropy__mean(),
        shanon_entropy__median=snippet_stats.shannon_entropy__median(),
        shanon_entropy__variance=snippet_stats.shannon_entropy__variance(),
        shanon_entropy__max= snippet_stats.shannon_entropy__max(),
        shanon_entropy__1Q= snippet_stats.shannon_entropy__1Q(),
        shanon_entropy__3Q= snippet_stats.shannon_entropy__3Q(),
    )
    return(snippet_features)

    



if __name__ == '__main__':
    # set package if
    
    make_feaures()
