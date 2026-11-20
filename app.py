import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="TCLS Dashboard | Yeshwanthpur", layout="wide", initial_sidebar_state="collapsed")
BASE=Path(__file__).parent
NAVY="#14264B"; BLUE="#3478E5"; TEAL="#13A394"; ORANGE="#F28C28"; PURPLE="#8050D8"
RED="#E64B5A"; CYAN="#1597B8"; YELLOW="#DDAA00"; INK="#253247"; MUTED="#657187"
units=pd.read_csv(BASE/"units.csv")
schools=pd.read_csv(BASE/"schools.csv")
trainers=pd.read_csv(BASE/"trainers.csv")
trainer_detail=pd.read_csv(BASE/"trainer_detail.csv")
skills=pd.read_csv(BASE/"skills.csv")
completion=pd.read_csv(BASE/"completion.csv")

st.markdown("""
<style>
.stApp{background:#F3F5F9;color:#253247}
.block-container{max-width:1500px;padding:.7rem 1rem 1rem}
header,footer{visibility:hidden}
.topbar{background:#14264B;color:white;border-radius:12px;padding:13px 20px;margin-bottom:10px}
.eyebrow{font-size:10px;letter-spacing:2px;color:#D4DDED;font-weight:700}
.heading{font-size:24px;font-weight:800;line-height:1.25;margin-top:4px}
.year{float:right;text-align:right;font-size:10px;letter-spacing:1px;color:#D4DDED}
.kpi{background:white;border:1px solid #E2E7EF;border-top:4px solid #3478E5;border-radius:11px;padding:10px 15px;min-height:78px}
.kpi .value{font-size:26px;font-weight:800;line-height:1.1;color:#17243D}
.kpi .label{font-size:10px;letter-spacing:1.2px;color:#657187;margin-top:5px;font-weight:700}
.panel{background:white;border:1px solid #E2E7EF;border-radius:12px;padding:11px 13px;margin-bottom:8px}
.panel-title{font-size:10px;letter-spacing:1.4px;color:#596579;font-weight:800;margin:0 0 5px}
div[data-testid="stMetric"]{background:#fff;border:1px solid #E2E7EF;border-radius:9px;padding:8px 10px}
div[data-testid="stMetricLabel"] p{color:#536176!important}
div[data-testid="stMetricValue"]{color:#17243D!important}
div[data-testid="stAlert"]{border-radius:10px}
</style>
""",unsafe_allow_html=True)

def panel_title(t):
    st.markdown(f'<div class="panel"><div class="panel-title">{t}</div></div>',unsafe_allow_html=True)
def chart_layout(fig,height=280,legend=False):
    fig.update_layout(height=height,margin=dict(l=5,r=25,t=5,b=5),
      font=dict(family="Arial",size=11,color=INK),paper_bgcolor="white",plot_bgcolor="white",
      showlegend=legend,xaxis=dict(title=None,showgrid=False,zeroline=False),
      yaxis=dict(title=None,showgrid=False,zeroline=False))
    return fig

# All headline KPIs are calculated from the eight updated source documents.
TOTAL_STUDENTS=int(units.Students_reported.sum())
TOTAL_CLASSES=int(units.Classes_reported.sum())
TOTAL_SKILLS_HEADLINE=int(units.Skills_headline_reported.sum())
TOTAL_TRAINERS=int(units.Trainers_reported.sum())
UG=int(units.UG_students.sum()); PG=int(units.PG_students.sum())

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
s=schools.copy()
school_members={
"Commerce":["Commerce"],
"Psychological Sciences":["Psychological Sciences"],
"Computer Science & Mathematics":["Computer Science","Mathematics"],
"Humanities and Performing Arts":["English","Media"],
"Professional Studies":["Professional Studies"],
"Social Sciences - Economics":["Social Sciences - Economics"]
}
school_values=[]
for school,members in school_members.items():
    school_values.append([school,int(u[u.Unit.isin(members)].Students_reported.sum())])
sf=pd.DataFrame(school_values,columns=["School","Students"])

# Filtered values for the unit-level panels.
f_skills=skills[skills.Unit.isin(selected)].copy()
f_completion=completion[completion.Unit.isin(selected)].copy()
f_trainers=trainer_detail[trainer_detail.Unit.isin(selected)].copy()
filtered_students=int(u.Students_reported.sum())
filtered_classes=int(u.Classes_reported.sum())
filtered_skills=int(u.Skills_headline_reported.sum())
filtered_trainers=int(u.Trainers_reported.sum())
filtered_ug=int(u.UG_students.sum()); filtered_pg=int(u.PG_students.sum())

kpis=[
 (f"{filtered_students:,}","TOTAL STUDENTS REPORTED",BLUE),
 (f"{filtered_trainers:,}","TRAINERS REPORTED",PURPLE),
 (f"{filtered_classes:,}","TOTAL CLASSES REPORTED",TEAL),
 (f"{filtered_skills:,}","SKILLS DELIVERED · HEADLINE TOTAL",ORANGE)]
cols=st.columns(4,gap="small")
for c,(v,l,color) in zip(cols,kpis):
    c.markdown(f'<div class="kpi" style="border-top-color:{color}"><div class="value">{v}</div><div class="label">{l}</div></div>',unsafe_allow_html=True)

st.write("")
left,mid,right=st.columns([1.05,1.5,1.0],gap="small")
with left:
    panel_title("STUDENTS BY SCHOOL")
    d=sf[sf.Students>0].sort_values("Students")
    fig=px.bar(d,x="Students",y="School",orientation="h",text="Students",color_discrete_sequence=[BLUE])
    fig.update_traces(textposition="outside",cliponaxis=False,textfont=dict(color=INK,size=10))
    chart_layout(fig,310)
    fig.update_layout(xaxis=dict(visible=False),yaxis=dict(tickfont=dict(size=10,color=INK)))
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

with mid:
    panel_title("CLASSES COMPLETING ONE OR TWO SKILLS")
    c=f_completion.melt(id_vars=["Unit"],value_vars=["One_skill_classes","Two_skill_classes"],
        var_name="Completion type",value_name="Classes")
    c=c.dropna(subset=["Classes"])
    c["Completion type"]=c["Completion type"].map({"One_skill_classes":"One skill","Two_skill_classes":"Two skills"})
    if not c.empty:
        fig=px.bar(c,x="Classes",y="Unit",color="Completion type",orientation="h",barmode="stack",
          text="Classes",color_discrete_map={"One skill":TEAL,"Two skills":BLUE})
        fig.update_traces(textposition="inside",textfont=dict(color="white",size=10))
        chart_layout(fig,310,True)
        fig.update_layout(xaxis=dict(visible=False),yaxis=dict(tickfont=dict(size=10,color=INK)),
          legend=dict(orientation="h",y=1.12,x=0,font=dict(color=INK,size=10)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.caption("Only numeric class counts entered in the completion tables are plotted. See data notes for source inconsistencies.")

with right:
    panel_title("TRAINER POOL")
    if not f_trainers.empty:
        t=f_trainers.groupby("Trainer_Type",as_index=False)["Count_reported"].sum()
        t=t[t.Count_reported>0]
        color_map={"External Trainers":BLUE,"CAPS / PhD Scholars":PURPLE,
                   "Digital Computer Science Department Trainers":TEAL,"Internal Department Trainers":ORANGE}
        fig=px.pie(t,names="Trainer_Type",values="Count_reported",hole=.62,color="Trainer_Type",
          color_discrete_map=color_map)
        fig.update_traces(textposition="inside",textinfo="percent",textfont=dict(color="white",size=10),
          hovertemplate="%{label}: %{value}<extra></extra>")
        fig.update_layout(height=245,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="white",
          font=dict(family="Arial",size=10,color=INK),
          legend=dict(orientation="v",y=-.02,x=0,font=dict(color=INK,size=9)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.metric("TRAINERS REPORTED IN SELECTED UNITS",f"{filtered_trainers:,}")

st.write("")
skill_col,ug_col=st.columns([1.25,1],gap="small")
with skill_col:
    panel_title("SKILLS DELIVERED BY TYPE")
    if not f_skills.empty:
        def skill_group(name):
            x=name.lower()
            if "financial" in x: return "Financial"
            if "entrepreneur" in x: return "Entrepreneurship"
            if "leadership" in x or "strategic thinking" in x: return "Leadership"
            if "digital" in x or "data" in x or "ai tools" in x: return "Digital"
            if "communication" in x or "writing" in x or "speaking" in x: return "Communication"
            if "aptitude" in x or "reasoning" in x: return "Aptitude"
            if "professional" in x or "career" in x: return "Professional"
            if "soft skill" in x or "multiple" in x: return "Multiple skill areas"
            return "Other"
        f_skills["Skill group"]=f_skills.Skill.apply(skill_group)
        palette={"Professional":BLUE,"Communication":TEAL,"Leadership":PURPLE,"Digital":CYAN,
                 "Aptitude":ORANGE,"Financial":YELLOW,"Entrepreneurship":RED,
                 "Multiple skill areas":"#6C83A8","Other":"#8A929E"}
        f_skills=f_skills.sort_values(["Skill group","Count_reported","Skill"],ascending=[True,False,True])
        fig=px.bar(f_skills,x="Count_reported",y="Skill",orientation="h",color="Skill group",
          text="Count_reported",color_discrete_map=palette,hover_data=["Unit","Source_note"])
        fig.update_traces(textposition="outside",cliponaxis=False,textfont=dict(color=INK,size=9))
        chart_layout(fig,max(620,24*len(f_skills)),True)
        fig.update_layout(xaxis=dict(visible=False),yaxis=dict(autorange="reversed",tickfont=dict(size=9,color=INK)),
          legend=dict(orientation="h",y=1.04,x=0,font=dict(color=INK,size=9)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        st.caption(f"{len(f_skills)} skill entries are listed from the source tables. Their displayed counts sum to {int(f_skills.Count_reported.sum())}; this differs from the 77 headline skill total. See data notes.")
with ug_col:
    panel_title("UNDERGRADUATE VS POSTGRADUATE STUDENTS")
    level=pd.DataFrame({"Level":["Undergraduate","Postgraduate"],"Students":[filtered_ug,filtered_pg]})
    c1,c2=st.columns([1,1.15],gap="small")
    with c1:
        fig=px.pie(level,names="Level",values="Students",hole=.62,color="Level",
          color_discrete_map={"Undergraduate":BLUE,"Postgraduate":ORANGE})
        fig.update_traces(textposition="inside",textinfo="percent",textfont=dict(color="white",size=11))
        fig.update_layout(height=250,margin=dict(l=0,r=0,t=0,b=0),showlegend=False,
          paper_bgcolor="white",font=dict(family="Arial",color=INK))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    with c2:
        st.metric("UNDERGRADUATE STUDENTS",f"{filtered_ug:,}")
        st.metric("POSTGRADUATE STUDENTS",f"{filtered_pg:,}")
        st.metric("TOTAL STUDENTS",f"{filtered_students:,}")

with st.expander("Detailed source figures and data-quality notes"):
    st.markdown("**Unit-level headline figures**")
    st.dataframe(u[["Unit","Students_reported","Classes_reported","Skills_headline_reported","UG_students","PG_students","Trainers_reported"]],hide_index=True,use_container_width=True)
    st.markdown("**All skills listed in the source documents**")
    st.dataframe(f_skills[["Unit","Skill","Count_reported","Source_note"]],hide_index=True,use_container_width=True)
    st.markdown("**Trainer breakdown**")
    st.dataframe(f_trainers,hide_index=True,use_container_width=True)
    st.markdown("**Class completion entries**")
    st.dataframe(f_completion,hide_index=True,use_container_width=True)
    st.markdown("""
**Data-quality notes — please read before official circulation**
- Student total is the sum of the eight unit headline figures: 2,542. UG/PG figures sum to 2,357 + 185 = 2,542.
- Class total is the sum of the eight headline figures: 45.
- Skills headline total is the sum of the eight headline figures: 77. The individual skill rows sum to 80. These are not the same measure and are not forced to reconcile.
- Source skill-table inconsistencies: Professional Studies lists skill rows totalling 7 but its table total says 30; Psychology lists rows totalling 16 while its headline says 12; Media lists rows totalling 22 while its headline says 12; Commerce lists skill rows totalling 11 while its headline says 22.
- Economics has two skill rows with blank names and count 2 each. They are shown as unspecified entries rather than assigned invented names.
- Trainer total 79 is the sum of the eight unit trainer totals. Reported categories sum to 64 External Trainers, 11 CAPS / PhD Scholars and 4 Digital Computer Science Department Trainers. Blank source cells are not assumed to be zero.
- The class-completion table contains numeric entries totalling 57 across one-skill and two-skill columns, exceeding the 45 headline classes. These are displayed as source-reported completion entries, not asserted to be 57 unique classes.
- Computer Science document's UG/PG table total row says 2 classes and 121 students, which conflicts with its headline (6 classes, 382 students) and level rows (4 UG + 2 PG classes; 261 UG + 121 PG students). Dashboard uses the headline and individual level rows, which reconcile to 382 students and 6 classes.
- Media has a blank one-skill class count despite listing 246 students in that column. The chart plots only its explicit two-skill class count of 12.
- Commerce trainer total row is blank; the listed External Trainers count is 11 and is included in the trainer sum.
- School totals are grouped from the reporting units: Computer Science & Mathematics combines Computer Science and Mathematics; Humanities and Performing Arts combines English and Media.
""")

st.markdown(f"""
<div style="background:#14264B;color:white;border-radius:10px;padding:9px 15px;margin-top:6px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:11px">
<span>TCLS Skill Development Dashboard · Yeshwanthpur Campus · Odd Semester · AY 2026–27</span>
<span><b>{TOTAL_STUDENTS:,}</b> Students &nbsp; <b>{TOTAL_CLASSES}</b> Classes &nbsp; <b>{TOTAL_TRAINERS}</b> Trainers</span>
</div>""",unsafe_allow_html=True)
