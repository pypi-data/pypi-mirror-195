# IBLearning

## Modules

### TextClustering
Allow text classification using KMeansCluster methods

#### Example
```python
from IBLearning.MachineLearning.KMeansCluster import TextClustering

# text to classify
texts = [
    "hello world",
    "this world is beautiful",
    "issou is a meme",
    "welcome to the world",
    "Risitas is the origin of issou",
    "Issou is a city in France"
]

# Create a TextClustering object
textClustering = TextClustering.TextClustering(TextClustering.Language.english)

# Add texts to the TextClustering object
for text in texts:
    textClustering.AddText(text)

# If needed, you can rebase the clusters with a new accuracy (create new clusters)
textClustering.RebaseClusterMean(accuracyMin=0.75)

# Get the clusters
clusters = textClustering.clusters

# Get the first cluster texts
texts = clusters[0].texts

# Get the first cluster words with count
words = clusters[0].words
```

### Possible improvements
- When processing a text mean, whe can use the word count to improve the accuracy of the mean