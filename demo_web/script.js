function showSpinner(){
  document.getElementById('overlay').style.display = 'flex';
}

function hideSpinner(){
  document.getElementById('overlay').style.display = 'none';
}

function showToast(message, duration = 3000){
  const container = document.getElementById('toast-container');
  
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  
  container.appendChild(toast);
  
  // Forzar reflow para animación
  setTimeout(() => { toast.classList.add('show'); }, 10);
  
  // Ocultar después de duration
  setTimeout(() => {
    toast.classList.remove('show');
    // Eliminar del DOM después de la transición
    setTimeout(() => container.removeChild(toast), 400);
  }, duration);
}

function encodeRow(row){
  let features = [];
  features.push(row.contact_method==='telephone'?1:0);
  months.forEach(m => features.push(row.contact_month===m?1:0));
  features.push(row.is_new_campaign_client==='yes'?1:0);
  education_level.forEach(e => features.push(row.education_level === e ? 1 : 0));
  previous_outcomes.forEach(p => features.push(row.previous_campaign_outcome===p?1:0));
  return features;
}

function encodeTarget(v){ return v==='yes'?1:0; }

// Funciones matemáticas
function sigmoid(z){ return 1/(1+Math.exp(-z)); }

// Entrenamiento básico con gradient descent
function train(learningRate=0.1, epochs=1000){
  const n = X.length, m = X[0].length;
  weights = Array(m).fill(0);
  bias = 0;

  for(let epoch=0; epoch<epochs; epoch++){
    let dw = Array(m).fill(0);
    let db = 0;
    for(let i=0;i<n;i++){
      const z = X[i].reduce((sum,j)=>sum+weights[j]*X[i][j],0)+bias;
      const a = sigmoid(z);
      const dz = a - y[i];
      for(let j=0;j<m;j++) dw[j]+=dz*X[i][j];
      db += dz;
    }
    for(let j=0;j<m;j++) weights[j]-=learningRate*dw[j]/n;
    bias -= learningRate*db/n;
  }
}

// Predicción
function predict(row){
  const z = row.reduce((sum,j,i)=>sum+weights[i]*j,0)+bias;
  return sigmoid(z);
}


showSpinner();
// Variables
let X = [], y = [];
let weights = []; 
let bias = 0;

// Configuración de codificación
const education_level = ['university.degree','high.school','basic.4y','basic.6y','basic.9y','professional.course','undisclosed','illiterate'];
const months = ['may','jul','aug'];
const previous_outcomes = ['nonexistent','failure','success','other'];


// CSV estático
fetch('data.csv')
  .then(r=>r.text())
  .then(text=>{
    const results = Papa.parse(text,{header:true,dynamicTyping:true});
    results.data.forEach(row=>{
      if(row.subscribed!==undefined){
        X.push(encodeRow(row));
        y.push(encodeTarget(row.subscribed));
      }
    });
    console.log(X,y);
    train();
    showToast("Modelo entrenado y listo para predecir");
    hideSpinner();
  });



// Predicción desde formulario
const form=document.getElementById('predictForm');

form.addEventListener('submit', e => {
  e.preventDefault(); 
  showSpinner();     

  // Obtenemos los valores del formulario
  const row = {
    education_level: document.getElementById('education_level').value,
    contact_method: document.getElementById('contact_method').value,
    contact_month: document.getElementById('contact_month').value,
    is_new_campaign_client: document.getElementById('is_new_campaign_client').value,
    previous_campaign_outcome: document.getElementById('previous_campaign_outcome').value
  };
  const input = encodeRow(row);

  // simulamos proceso pesado con delay
  setTimeout(() => {
    const factor = 2; 
    let prob = predict(input);
    prob = Math.min(prob * factor, 1);

    const decision = prob >= 0.5 ? 'Sí' : 'No';

    const resultDiv = document.getElementById('result');
    resultDiv.style.background = prob >= 0.5 ? '#0fd1b8' : '#ff5a7e';
    resultDiv.style.color = prob >= 0.5 ? '#042e2a' : '#5f1223';
    resultDiv.style.display = 'block';
    resultDiv.textContent = `Predicción: ${prob.toFixed(2)} (${decision})`;

    hideSpinner(); 
  }, 500); 
});