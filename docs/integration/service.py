from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from adapter import infer,CARD
app=FastAPI(title='SENSIpred educational adapter',version='demo-v1')
class Input(BaseModel):
 query:str=Field(min_length=1,max_length=4096)
@app.get('/models')
def models():return {'available_models':[CARD['model_id']],'details':{CARD['model_id']:{k:CARD[k] for k in ['endpoint','assay','target','threshold','calibration','ad']}}}
@app.post('/predict/{model_id}')
def prediction(model_id:str,data:Input):
 try:return infer(data.query,model_id)
 except KeyError as e:raise HTTPException(404,detail=str(e)) from e
 except ValueError as e:raise HTTPException(422,detail=str(e)) from e
# Production async jobs, resolver and authentication stay in the existing platform.
