let responseChart, cohortChart, currentItems = [];
const fmt = n => Number(n).toLocaleString(undefined,{maximumFractionDigits:1});
async function loadSummary(){
 const s=await fetch('/api/summary').then(r=>r.json());
 document.getElementById('total').textContent=fmt(s.total_samples);
 document.getElementById('cd4').textContent=fmt(s.averages.cd4);
 document.getElementById('cd8').textContent=fmt(s.averages.cd8);
 document.getElementById('inflam').textContent=Number(s.averages.inflammation).toFixed(2);
 const common={responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{usePointStyle:true,boxWidth:8,padding:18,font:{size:11}}}}};
 responseChart=new Chart(document.getElementById('responseChart'),{type:'doughnut',data:{labels:s.response_groups.map(x=>x.label),datasets:[{data:s.response_groups.map(x=>x.value),backgroundColor:['#258a83','#f1b85a','#d77b7b'],borderWidth:0,hoverOffset:5}]},options:{...common,cutout:'68%'}});
 cohortChart=new Chart(document.getElementById('cohortChart'),{type:'bar',data:{labels:s.cohorts.map(x=>x.label),datasets:[{label:'Samples',data:s.cohorts.map(x=>x.value),backgroundColor:['#1c817b','#74bdb4','#a9d9d3'],borderRadius:6,borderSkipped:false}]},options:{...common,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true,ticks:{precision:0},grid:{color:'#edf1f5'}}}}});
}
async function loadSamples(){
 const q=new URLSearchParams({q:document.getElementById('search').value,cohort:document.getElementById('cohort').value,response_group:document.getElementById('response').value});
 const data=await fetch('/api/samples?'+q).then(r=>r.json()); currentItems=data.items;
 const tbody=document.getElementById('sampleRows');
 if(!data.items.length){tbody.innerHTML='<tr><td colspan="8">No matching samples found.</td></tr>'}
 else tbody.innerHTML=data.items.map(x=>`<tr><td class="sample-id">${x.sample_code}</td><td>${x.cohort}</td><td>${x.collection_date}</td><td>${fmt(x.cd4_count)}</td><td>${fmt(x.cd8_count)}</td><td>${x.b_cell_pct}%</td><td>${x.inflammation_score.toFixed(2)}</td><td><span class="pill ${x.response_group.toLowerCase().replaceAll(' ','-')}">${x.response_group}</span></td></tr>`).join('');
 document.getElementById('tableFoot').textContent=`Showing ${data.count} records · Up to 200 results`;
}
['search','cohort','response'].forEach(id=>document.getElementById(id).addEventListener(id==='search'?'input':'change',loadSamples));
document.getElementById('exportBtn').addEventListener('click',()=>{
 const cols=['sample_code','cohort','collection_date','cd4_count','cd8_count','b_cell_pct','inflammation_score','response_group'];
 const csv=[cols.join(','),...currentItems.map(row=>cols.map(k=>JSON.stringify(row[k]??'')).join(','))].join('\n');
 const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8;'})); const a=document.createElement('a');a.href=url;a.download='immune-samples.csv';a.click();URL.revokeObjectURL(url);
});
loadSummary().catch(console.error);loadSamples().catch(console.error);