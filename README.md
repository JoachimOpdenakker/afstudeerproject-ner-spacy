<!-- # afstudeerproject-ner-spacy -->
Op de onderstaande link vindt u de stappen die wij hebben gedaan om ons model te trainen
## [Research jupyter notebook](research.ipynb)




## File structuur
### [Config](config)
Hier vindt u de files die temaken hebben met de configuratie van het model
...[Customtokenizer.py](config/CustomTokenizer.py)..

Dit is onze eigen gemaakte Tokenizer, deze gaat ervoor zorgen dat "," altijd als een aparte token gezien wordt.
![image](https://user-images.githubusercontent.com/43540060/156184112-2586d7ab-17ef-4def-a459-ad47cc875532.png)

### [Data](data)
Hier vindt u 2 submappen [Samples](samples) en [TrainingData](trainingData)

In het mapje samples vindt u steekproeven op adressen van verschillende groottes.

In het mapje trainingData vindt u de trainingsdata van veel adressen die wij gebruiken.

### [Model](model)
Hier vindt u 2 mappen met daarin het beste (gebruikte) model en de laatste (gebruikte) model.  

### [Scripts](scripts)
Hier vindt u onze gebruikte python scripts (meer info vindt u in onze jupyter notebook)

