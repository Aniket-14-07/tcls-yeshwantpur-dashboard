import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="TCLS Dashboard | Yeshwanthpur", layout="wide", initial_sidebar_state="collapsed")
NAVY="#14264B"; BLUE="#3478E5"; TEAL="#13A394"; ORANGE="#F28C28"; PURPLE="#8050D8"; RED="#E64B5A"
INK="#253247"; MUTED="#657187"; GRID="#E8ECF3"
BASE=Path(__file__).parent
units=pd.read_csv(BASE/"units.csv")
schools=pd.read_csv(BASE/"schools.csv")
trainer_detail=pd.read_csv(BASE/"trainer_detail.csv")
skills=pd.read_csv(BASE/"skills.csv")

st.markdown("""
<style>
.stApp{background:#F3F5F9;color:#253247}
.block-container{max-width:1500px;padding:.7rem 1rem 1rem}
header,footer{visibility:hidden}
.topbar{background:#14264B;color:white;border-radius:12px;padding:12px 20px;margin-bottom:10px}
.eyebrow{font-size:10px;letter-spacing:2px;color:#D4DDED;font-weight:700}
.heading{font-size:24px;font-weight:800;line-height:1.25;margin-top:4px}
.year{float:right;text-align:right;font-size:10px;letter-spacing:1px;color:#D4DDED}
.kpi{background:white;border:1px solid #E2E7EF;border-top:4px solid #3478E5;border-radius:11px;padding:10px 15px;min-height:76px}
.kpi .value{font-size:26px;font-weight:800;line-height:1.1;color:#17243D}
.kpi .label{font-size:10px;letter-spacing:1.2px;color:#657187;margin-top:5px;font-weight:700}
.panel{background:white;border:1px solid #E2E7EF;border-radius:12px;padding:11px 13px;margin-bottom:8px}
.panel-title{font-size:10px;letter-spacing:1.4px;color:#596579;font-weight:800;margin:0 0 5px}
div[data-testid="stMetric"]{background:#fff;border:1px solid #E2E7EF;border-radius:9px;padding:8px 10px}
div[data-testid="stMetricLabel"] p{color:#536176!important}
div[data-testid="stMetricValue"]{color:#17243D!important}
</style>
""",unsafe_allow_html=True)

def title(t):
    st.markdown(f'<div class="panel"><div class="panel-title">{t}</div></div>',unsafe_allow_html=True)
def layout(fig,height=280,legend=False):
    fig.update_layout(height=height,margin=dict(l=5,r=22,t=5,b=5),
      font=dict(family="Arial",size=11,color=INK),paper_bgcolor="white",plot_bgcolor="white",
      showlegend=legend,
      xaxis=dict(title=None,showgrid=False,zeroline=False,tickfont=dict(color=INK)),
      yaxis=dict(title=None,showgrid=False,zeroline=False,tickfont=dict(color=INK)))
    return fig

st.markdown("""
<div class="topbar">
 <div class="year">ACADEMIC YEAR<br><b>AY 2026–27</b></div>
 <div class="eyebrow">TRAINING FOR CAREER &amp; LIFE SKILLS — DASHBOARD</div>
 <div class="heading">Yeshwanthpur Campus · Odd Semester</div>
</div>""",unsafe_allow_html=True)

with st.sidebar:
    st.header("Dashboard filters")
    selected=st.multiselect("Select reporting units",units.Unit.tolist(),default=units.Unit.tolist())
    st.caption("Filters apply to unit-level charts and detailed tables.")
u=units[units.Unit.isin(selected)]
students=int(u.Students.sum())
classes=int(u.Classes_reported.sum())
skills_count=int(u.Skills_reported.sum())
hours=int(u.Training_hours.fillna(0).sum())
level_map={
"Commerce":(712,0),"English":(0,20),"Mathematics":(117,0),"Media":(227,19),
"B.Sc. Psychology":(275,0),"DPS":(334,0),"Economics":(161,25),"CS Odd_PG":(261,121)}
ug=sum(level_map[x][0] for x in selected); pg=sum(level_map[x][1] for x in selected)
td=trainer_detail[trainer_detail.Unit.isin(selected)]
trainer_total=int(td.Trainers.sum())

cards=[
 (f"{students:,}","STUDENTS REPORTED",BLUE),
 (f"{classes:,}","CLASSES REPORTED",PURPLE),
 (f"{hours:,}","COMMERCE TRAINING HOURS",TEAL),
 (f"{trainer_total:,}","TRAINERS REPORTED",ORANGE)]
cols=st.columns(4,gap="small")
for c,(v,l,col) in zip(cols,cards):
    c.markdown(f'<div class="kpi" style="border-top-color:{col}"><div class="value">{v}</div><div class="label">{l}</div></div>',unsafe_allow_html=True)
st.write("")

# School totals are grouped from source unit headcounts; filtering keeps the school grouping consistent.
school_units={
"Commerce":["Commerce"],"Psychological Sciences":["B.Sc. Psychology"],
"Computer Science & Mathematics":["Mathematics","CS Odd_PG"],
"Humanities & Performing Arts":["English","Media"],
"Professional Studies":["DPS"],"Social Sciences – Economics":["Economics"]}
school_rows=[]
for school, members in school_units.items():
    school_rows.append([school,int(units[units.Unit.isin([x for x in members if x in selected])].Students.sum())])
sf=pd.DataFrame(school_rows,columns=["School","Students"])
left,mid,right=st.columns([1.05,1.5,1.0],gap="small")
with left:
    title("STUDENTS BY SCHOOL")
    d=sf[sf.Students>0].sort_values("Students")
    fig=px.bar(d,x="Students",y="School",orientation="h",text="Students",color_discrete_sequence=[BLUE])
    fig.update_traces(textposition="outside",cliponaxis=False,textfont=dict(color=INK,size=10))
    layout(fig,300); fig.update_layout(xaxis=dict(visible=False),yaxis=dict(tickfont=dict(size=10,color=INK)))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
with mid:
    title("CLASSES COMPLETING ONE OR TWO SKILLS")
    completion=pd.DataFrame([
      ["Commerce",0,11],["Mathematics",0,2],["Media",10,10],
      ["B.Sc. Psychology",0,4],["CS Odd_PG",0,12]
    ],columns=["Unit","One skill","Two skills"])
    completion=completion[completion.Unit.isin(selected)]
    long=completion.melt(id_vars="Unit",var_name="Completion",value_name="Classes")
    fig=px.bar(long,x="Classes",y="Unit",color="Completion",orientation="h",barmode="stack",text="Classes",
      color_discrete_map={"One skill":TEAL,"Two skills":BLUE})
    fig.update_traces(textposition="inside",textfont=dict(color="white",size=10))
    layout(fig,300,True)
    fig.update_layout(xaxis=dict(visible=False),yaxis=dict(tickfont=dict(size=10,color=INK)),
      legend=dict(orientation="h",y=1.12,x=0,font=dict(color=INK,size=10)))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.caption("Only explicit numeric class counts are plotted. English has no numeric completion count; DPS reports hours; Economics lists class/section names without a clear numeric total.")
with right:
    title("TRAINER POOL")
    if not td.empty:
        t=td.groupby("Trainer_Type",as_index=False).Trainers.sum()
        fig=px.pie(t,names="Trainer_Type",values="Trainers",hole=.62,
          color="Trainer_Type",color_discrete_map={"External Trainers":BLUE,"CAPS / PhD Scholars":PURPLE,
          "Digital CS-Department Trainers":TEAL,"Internal Department Trainers":ORANGE})
        fig.update_traces(textposition="inside",textinfo="percent",textfont=dict(color="white",size=10),
          hovertemplate="%{label}: %{value}<extra></extra>")
        fig.update_layout(height=235,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="white",
          font=dict(family="Arial",size=10,color=INK),legend=dict(orientation="v",y=-.02,x=0,font=dict(color=INK,size=9)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.metric("TOTAL TRAINERS REPORTED",f"{trainer_total:,}")

st.write("")
a,b=st.columns([1.05,1.55],gap="small")
with a:
    title("SKILLS REPORTED BY UNIT")
    d=u.sort_values("Skills_reported")
    fig=px.bar(d,x="Skills_reported",y="Unit",orientation="h",text="Skills_reported",color_discrete_sequence=[PURPLE])
    fig.update_traces(textposition="outside",cliponaxis=False,textfont=dict(color=INK,size=10))
    layout(fig,270); fig.update_layout(xaxis=dict(visible=False),yaxis=dict(tickfont=dict(size=10,color=INK)))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.caption(f"{skills_count} is the sum of the unit-level headline fields, not a deduplicated count of unique skill names.")
with b:
    title("UNDERGRADUATE VS POSTGRADUATE STUDENTS")
    level=pd.DataFrame({"Level":["Undergraduate","Postgraduate"],"Students":[ug,pg]})
    c1,c2=st.columns([1,1.25],gap="small")
    with c1:
        fig=px.pie(level,names="Level",values="Students",hole=.62,color="Level",
          color_discrete_map={"Undergraduate":BLUE,"Postgraduate":ORANGE})
        fig.update_traces(textposition="inside",textinfo="percent",textfont=dict(color="white",size=11))
        fig.update_layout(height=245,margin=dict(l=0,r=0,t=0,b=0),showlegend=False,
          paper_bgcolor="white",font=dict(family="Arial",color=INK))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        st.metric("UNDERGRADUATE STUDENTS",f"{ug:,}")
        st.metric("POSTGRADUATE STUDENTS",f"{pg:,}")
        st.metric("TOTAL STUDENTS",f"{students:,}")

with st.expander("Detailed source data and official reporting notes"):
    st.markdown("**Unit-level headline figures**")
    st.dataframe(u[["Unit","Students","Classes_reported","Skills_reported","Training_hours"]],hide_index=True,use_container_width=True)
    st.markdown("**Skill entries as written in the source documents**")
    st.dataframe(skills[skills.Unit.isin(selected)],hide_index=True,use_container_width=True)
    st.markdown("**Trainer breakdown from the source documents**")
    st.dataframe(td,hide_index=True,use_container_width=True)
    st.markdown("""
**Definitions and limitations**
- The eight source documents sum to 2,272 student records. The documents do not establish whether the records overlap; this is therefore labelled “students reported”, not unique students.
- Total classes = 45, calculated from each unit's UG/PG class split or headline class count. Commerce reports 330 Hrs in its headline field but separately reports 11 UG classes (6 + 5); 330 is not counted as classes.
- Commerce training hours are shown separately as 330.
- UG/PG student split: 2,087 undergraduate and 185 postgraduate students, using the individual source level figures.
- Trainer total: 58 external trainers + 11 CAPS/PhD scholars + 2 digital CS-department trainers = 71. Blank source fields are not treated as confirmed zeroes.
- Skill headline total 42 is the sum of unit-level headline fields. Skill-type counts differ in unit and should not be added as a common measure.
- Completion chart includes only explicit numeric class counts. DPS reports 15+15 hours, Economics gives named sections without an unambiguous numeric class total, and English does not give a numeric completion count. The chart's one-skill/two-skill entries are source-reported counts and are not assumed to be unique classes across categories.
- CS Odd_PG has an inconsistent total row in its UG/PG class table. Its separately stated UG 261 and PG 121 student figures reconcile to the 382 headline total.
""")

st.markdown(f"""
<div style="background:#14264B;color:white;border-radius:10px;padding:9px 15px;margin-top:6px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:11px">
<span>TCLS Skill Development Dashboard · Yeshwanthpur Campus · Odd Semester · AY 2026–27</span>
<span><b>{students:,}</b> Students &nbsp; <b>{classes}</b> Classes &nbsp; <b>{trainer_total}</b> Trainers</span>
</div>""",unsafe_allow_html=True)
