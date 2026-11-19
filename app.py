import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="TCLS Dashboard | Yeshwanthpur", layout="wide")
NAVY="#14264B"; BLUE="#3478E5"; TEAL="#13A394"; ORANGE="#F28C28"; PURPLE="#8050D8"; RED="#E64B5A"
st.markdown("""
<style>
.block-container{padding-top:1rem;padding-bottom:1rem;max-width:1500px}
header{visibility:hidden}
.topbar{background:#14264B;color:white;border-radius:12px;padding:12px 20px;margin-bottom:10px}
.topbar small{letter-spacing:2px;color:#cbd5e1}
.topbar h2{margin:3px 0 0 0;font-size:25px}
.kpi{background:white;border:1px solid #e3e8f0;border-top:4px solid #3478E5;border-radius:12px;padding:10px 16px;min-height:78px}
.kpi .n{font-size:27px;font-weight:800;color:#17243d;line-height:1.1}
.kpi .l{font-size:10px;letter-spacing:1.5px;color:#667085;margin-top:5px}
.panel{background:white;border:1px solid #e3e8f0;border-radius:13px;padding:13px 15px;margin-bottom:10px}
.panel h4{font-size:11px;letter-spacing:1.4px;color:#596579;margin:0 0 8px 0}
div[data-testid="stAppViewContainer"]{background:#f3f5f9}
div[data-testid="stMetric"]{background:white;border:1px solid #e3e8f0;border-radius:10px;padding:10px}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

def read_csv(name): return pd.read_csv(Path(__file__).parent/name)
units=read_csv("units.csv"); schools=read_csv("schools.csv"); trainers=read_csv("trainers.csv"); skills=read_csv("skills.csv")
st.markdown('<div class="topbar"><small>TRAINING FOR CAREER & LIFE SKILLS — DASHBOARD</small><h2>Yeshwanthpur Campus · Odd Semester</h2><div style="text-align:right;font-size:12px;color:#dce5f5">ACADEMIC YEAR&nbsp;&nbsp; <b>AY 2026–27</b></div></div>',unsafe_allow_html=True)

with st.sidebar:
    st.header("Dashboard filters")
    chosen=st.multiselect("Select units",units.Unit.tolist(),default=units.Unit.tolist())
    st.caption("Select one or more reporting units to filter the dashboard.")
u=units[units.Unit.isin(chosen)]
s=schools.copy()
# School totals are sourced from unit student totals; adjust by selected reporting units.
school_map={
"Commerce":["Commerce"],"Psychological Sciences":["B.Sc. Psychology"],
"Computer Science & Mathematics":["Mathematics","CS Odd_PG"],
"Humanities & Performing Arts":["Media","English"],
"Professional Studies":["DPS"],"Social Sciences – Economics":["Economics"]}
s["Students"]=s.apply(lambda r: sum(int(units.loc[units.Unit.eq(x),"Students"].sum()) for x in school_map[r.School] if x in chosen),axis=1)
t=units[units.Unit.isin(chosen)]
# Headline class count uses the user's requested reporting convention: Commerce = 330 classes.
students=int(t.Students.sum()); classes=int(t.Classes.sum()); skills_total=int(t["Skills reported"].sum())
trainers_total=int(trainers.Trainers.sum()) if len(chosen)==len(units) else int(units.loc[units.Unit.isin(chosen),"Trainers"].sum())
k=st.columns(4)
for col,num,label,color in zip(k,[f"{students:,}",f"{classes:,}",f"{skills_total:,}",f"{trainers_total:,}"],["TOTAL STUDENTS","TOTAL CLASSES","SKILLS REPORTED","TRAINERS"],[BLUE,PURPLE,TEAL,ORANGE]):
    col.markdown(f'<div class="kpi" style="border-top-color:{color}"><div class="n">{num}</div><div class="l">{label}</div></div>',unsafe_allow_html=True)

left,mid,right=st.columns([1.05,1.55,1.0],gap="small")
with left:
    st.markdown('<div class="panel"><h4>STUDENTS BY SCHOOL</h4></div>',unsafe_allow_html=True)
    splot=s[s.Students>0].sort_values("Students")
    fig=px.bar(splot,x="Students",y="School",orientation="h",text="Students",color_discrete_sequence=[BLUE])
    fig.update_traces(textposition="outside",cliponaxis=False)
    fig.update_layout(height=300,margin=dict(l=5,r=30,t=5,b=5),showlegend=False,xaxis=dict(visible=False),yaxis=dict(title=None,tickfont=dict(size=10)),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
with mid:
    st.markdown('<div class="panel"><h4>CLASSES AND STUDENTS BY REPORTING UNIT</h4></div>',unsafe_allow_html=True)
    plot=u.sort_values("Students")
    fig=px.bar(plot,x="Students",y="Unit",orientation="h",text="Students",color="Unit",color_discrete_sequence=[TEAL,BLUE,PURPLE,ORANGE,RED])
    fig.update_traces(textposition="outside",cliponaxis=False)
    fig.update_layout(height=300,margin=dict(l=5,r=35,t=5,b=5),showlegend=False,xaxis=dict(visible=False),yaxis=dict(title=None,tickfont=dict(size=10)),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
with right:
    st.markdown('<div class="panel"><h4>TRAINER POOL</h4></div>',unsafe_allow_html=True)
    td= trainers.copy()
    if len(chosen)!=len(units):
        # Unit-level trainer totals cannot be disaggregated by category reliably from all files.
        st.metric("Trainers in selected units",trainers_total)
        st.caption("Trainer-type breakdown is shown only for the full combined dataset.")
    else:
        fig=px.pie(td,values="Trainers",names="Trainer Type",hole=.62,color_discrete_sequence=[BLUE,PURPLE,TEAL,ORANGE])
        fig.update_layout(height=235,margin=dict(l=0,r=0,t=0,b=0),legend=dict(orientation="h",y=-.1,font=dict(size=9)),paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.metric("TOTAL TRAINERS",trainers_total)

# One/two-skill completion counts are shown only where the source reports numeric class counts.
st.markdown('<div class="panel"><h4>CLASSES THAT COMPLETED ONE AND TWO SKILLS</h4></div>',unsafe_allow_html=True)
completion_rows = [
    ["Commerce",0,11],["English",0,2],["Mathematics",0,2],
    ["Media",10,10],["B.Sc. Psychology",0,4],["CS Odd_PG",0,12]
]
completion = pd.DataFrame(completion_rows, columns=["Unit","One skill","Two skills"])
completion = completion[completion.Unit.isin(chosen)]
if not completion.empty:
    comp_long = completion.melt(id_vars="Unit",var_name="Completion type",value_name="Classes")
    fig=px.bar(comp_long,x="Classes",y="Unit",color="Completion type",orientation="h",barmode="stack",
               color_discrete_map={"One skill":TEAL,"Two skills":BLUE},text="Classes")
    fig.update_traces(textposition="inside")
    fig.update_layout(height=235,margin=dict(l=5,r=15,t=5,b=5),legend=dict(orientation="h",y=1.12),
                      xaxis=dict(visible=False),yaxis=dict(title=None,tickfont=dict(size=10)),
                      paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
st.caption("Only numeric class counts are plotted; DPS reports hours and Economics provides class names rather than a numeric count, so those entries are not converted.")

a,b=st.columns([1.05,1.55],gap="small")
with a:
    st.markdown('<div class="panel"><h4>SKILLS REPORTED BY UNIT</h4></div>',unsafe_allow_html=True)
    sd=skills[skills.Unit.isin(chosen)].groupby("Unit",as_index=False).Count.sum().sort_values("Count")
    fig=px.bar(sd,x="Count",y="Unit",orientation="h",text="Count",color_discrete_sequence=[PURPLE])
    fig.update_traces(textposition="outside",cliponaxis=False)
    fig.update_layout(height=265,margin=dict(l=5,r=30,t=5,b=5),showlegend=False,xaxis=dict(visible=False),yaxis=dict(title=None,tickfont=dict(size=10)),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
with b:
    st.markdown('<div class="panel"><h4>UNDERGRADUATE VS POSTGRADUATE STUDENTS</h4></div>',unsafe_allow_html=True)
    # Student counts by level from the supplied documents.
    level_rows={"Commerce":(712,0),"English":(0,20),"Mathematics":(117,0),"Media":(227,19),"B.Sc. Psychology":(275,0),"DPS":(334,0),"Economics":(161,25),"CS Odd_PG":(261,121)}
    ug=sum(level_rows[x][0] for x in chosen); pg=sum(level_rows[x][1] for x in chosen)
    pie=pd.DataFrame({"Level":["Undergraduate","Postgraduate"],"Students":[ug,pg]})
    c1,c2=st.columns([1,1.4])
    with c1:
        fig=px.pie(pie,values="Students",names="Level",hole=.62,color_discrete_sequence=[BLUE,ORANGE])
        fig.update_layout(height=225,margin=dict(l=0,r=0,t=0,b=0),showlegend=False,paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        st.metric("Undergraduate students",f"{ug:,}")
        st.metric("Postgraduate students",f"{pg:,}")
        st.caption(f"Total: {ug+pg:,} students")

st.markdown('<div class="panel"><h4>SKILL-WISE DETAIL · REPORTED COUNTS AS ENTERED IN SOURCE DOCUMENTS</h4></div>',unsafe_allow_html=True)
sd=skills[skills.Unit.isin(chosen)].sort_values("Count",ascending=False)
st.dataframe(sd,hide_index=True,use_container_width=True,height=245)
with st.expander("Data notes and source limitations"):
    st.write("All eight submitted Word documents are represented. The Commerce headline value is treated as 330 classes as requested, although its source document labels it '330 Hrs'.")
    st.write("Student total is the sum of the eight document headline values (2,272); it may include overlap if students appear in more than one reporting unit.")
    st.write("Skill counts are preserved as recorded. The source documents mix class counts, student counts and other reporting units, so they should not be interpreted as one uniform measure.")
    st.write("The documents report different levels of detail for completion of one/two skills and trainer categories. Blank fields are not automatically treated as zero.")
st.caption("TCLS · Yeshwanthpur Campus · Odd Semester · AY 2026–27")
