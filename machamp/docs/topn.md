### Output the top-n predictions
[back to main README](../README.md)

To output the top-n predictions and their probabilities `--topn` can be used
when using `predict.py`. This feature is only implemented for the task-type
`seq` and `classification` for now. Example usage:

```
python3 predict.py logs/ewt/2021.12.14_13.32.40/model.tar.gz data/ewt.dev out --topn 10
```

The output will look like:
```
# newdoc id = weblog-blogspot.com_nominations_20041117172713_ENG_20041117_172713
# sent_id = weblog-blogspot.com_nominations_20041117172713_ENG_20041117_172713-0001
# newpar id = weblog-blogspot.com_nominations_20041117172713_ENG_20041117_172713-p0001
# text = From the AP comes this story :
1	From	from	ADP=0.9999890327453613|SCONJ=3.0365351904038107e-06
2	the	the	DET=0.9999867677688599|PRON=6.264202056627255e-06
3	AP	ap	NOUN=0.6444783806800842|PROPN=0.3552662134170532
4	comes	come	VERB=0.9999005794525146|NOUN=3.860901779262349e-05
5	this	this	DET=0.9999325275421143|PRON=6.400897109415382e-05
6	story	story	NOUN=0.9999674558639526|PROPN=1.901647192426026e-05

```
