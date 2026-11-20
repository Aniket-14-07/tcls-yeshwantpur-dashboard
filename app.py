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

def build_dashboard_pdf(units_df, school_df, completion_df, trainer_df, skills_df):
    """Create a compact, single-page A3 landscape snapshot of the filtered dashboard."""
    from io import BytesIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A3, landscape
    from reportlab.lib import colors
    from reportlab.pdfbase.pdfmetrics import stringWidth

    W, H = landscape(A3)
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=(W, H))
    C = {
        "navy": colors.HexColor("#14264B"), "blue": colors.HexColor("#3478E5"),
        "teal": colors.HexColor("#13A394"), "orange": colors.HexColor("#F28C28"),
        "purple": colors.HexColor("#8050D8"), "red": colors.HexColor("#E64B5A"),
        "cyan": colors.HexColor("#1597B8"), "yellow": colors.HexColor("#DDAA00"),
        "ink": colors.HexColor("#253247"), "muted": colors.HexColor("#657187"),
        "line": colors.HexColor("#E2E7EF"), "bg": colors.HexColor("#F3F5F9"),
        "white": colors.white, "grey": colors.HexColor("#8A929E")
    }
    group_colors = {"Professional": C["blue"], "Communication": C["teal"],
        "Leadership": C["purple"], "Digital": C["cyan"], "Aptitude": C["orange"],
        "Financial": C["yellow"], "Entrepreneurship": C["red"],
        "Multiple skill areas": colors.HexColor("#6C83A8"), "Other": C["grey"]}

    def txt(x, y, value, size=8, color=None, bold=False):
        c.setFillColor(color or C["ink"])
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, str(value))

    def fit_text(value, max_width, size=7, bold=False):
        value = str(value)
        font = "Helvetica-Bold" if bold else "Helvetica"
        while size > 5 and stringWidth(value, font, size) > max_width:
            size -= .25
        if stringWidth(value, font, size) > max_width:
            while value and stringWidth(value + "…", font, size) > max_width:
                value = value[:-1]
            value += "…"
        return value, size

    def panel(x, y, w, h, title):
        c.setFillColor(C["white"]); c.setStrokeColor(C["line"]); c.setLineWidth(.8)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
        txt(x+12, y+h-19, title.upper(), 8, C["muted"], True)
        c.setStrokeColor(C["line"]); c.line(x+12, y+h-26, x+w-12, y+h-26)

    def skill_group(name):
        x = str(name).lower()
        if "financial" in x: return "Financial"
        if "entrepreneur" in x: return "Entrepreneurship"
        if "leadership" in x or "strategic thinking" in x: return "Leadership"
        if "digital" in x or "data" in x or "ai tools" in x: return "Digital"
        if "communication" in x or "writing" in x or "speaking" in x: return "Communication"
        if "aptitude" in x or "reasoning" in x: return "Aptitude"
        if "professional" in x or "career" in x: return "Professional"
        if "soft skill" in x or "multiple" in x: return "Multiple skill areas"
        return "Other"

    total_students = int(units_df.Students_reported.sum())
    total_trainers = int(units_df.Trainers_reported.sum())
    total_classes = int(units_df.Classes_reported.sum())
    total_skills = int(units_df.Skills_headline_reported.sum())
    ug = int(units_df.UG_students.sum()); pg = int(units_df.PG_students.sum())

    # Page background and header
    c.setFillColor(C["bg"]); c.rect(0, 0, W, H, fill=1, stroke=0)
    margin = 25
    c.setFillColor(C["navy"]); c.roundRect(margin, H-77, W-2*margin, 52, 9, fill=1, stroke=0)
    txt(margin+16, H-45, "TRAINING FOR CAREER & LIFE SKILLS — DASHBOARD", 8, colors.HexColor("#D4DDED"), True)
    txt(margin+16, H-65, "Yeshwanthpur Campus · Odd Semester", 17, C["white"], True)
    txt(W-margin-125, H-45, "ACADEMIC YEAR", 7, colors.HexColor("#D4DDED"), True)
    txt(W-margin-125, H-62, "AY 2026–27", 10, C["white"], True)

    # KPI cards
    kpis = [(f"{total_students:,}", "STUDENTS REPORTED", C["blue"]),
            (f"{total_trainers:,}", "TRAINERS REPORTED", C["purple"]),
            (f"{total_classes:,}", "CLASSES REPORTED", C["teal"]),
            (f"{total_skills:,}", "SKILLS · HEADLINE TOTAL", C["orange"])]
    gap = 10; card_y = H-133; card_h = 45; card_w = (W-2*margin-3*gap)/4
    for i, (value, label, accent) in enumerate(kpis):
        x = margin+i*(card_w+gap)
        c.setFillColor(C["white"]); c.setStrokeColor(C["line"]); c.roundRect(x, card_y, card_w, card_h, 7, fill=1, stroke=1)
        c.setFillColor(accent); c.roundRect(x, card_y+card_h-4, card_w, 4, 2, fill=1, stroke=0)
        txt(x+12, card_y+22, value, 17, C["ink"], True)
        txt(x+12, card_y+9, label, 7, C["muted"], True)

    # Upper row panels
    top_y, top_h = H-367, 218
    x1, w1 = margin, 330
    x2, w2 = x1+w1+10, 475
    x3, w3 = x2+w2+10, W-margin-(x2+w2+10)
    panel(x1, top_y, w1, top_h, "Students by school")
    d = school_df[school_df.Students > 0].sort_values("Students", ascending=True)
    maxv = max([int(v) for v in d.Students] or [1]); rows = max(len(d), 1)
    row_h =  (top_h-43)/rows
    for i, row in enumerate(d.itertuples(index=False)):
        yy = top_y+12+i*row_h
        label, fs = fit_text(row.School, 125, 7)
        txt(x1+12, yy+3, label, fs)
        bx=x1+143; bw=w1-183; barw=bw*int(row.Students)/maxv
        c.setFillColor(colors.HexColor("#E9EEF6")); c.roundRect(bx, yy, bw, 9, 3, fill=1, stroke=0)
        c.setFillColor(C["blue"]); c.roundRect(bx, yy, max(2,barw), 9, 3, fill=1, stroke=0)
        txt(bx+bw+5, yy+2, f"{int(row.Students):,}", 7, C["ink"], True)

    panel(x2, top_y, w2, top_h, "Classes completing one or two skills")
    comp = completion_df.copy()
    if not comp.empty:
        comp = comp.fillna(0)
        comp = comp[(comp.One_skill_classes.astype(float)>0)|(comp.Two_skill_classes.astype(float)>0)]
    n=max(len(comp),1); rh=(top_h-45)/n
    maxcomp=max([float(v) for v in list(comp.get("One_skill_classes",[]))+list(comp.get("Two_skill_classes",[]))] or [1])
    maxstack=max([float(a)+float(b) for a,b in zip(comp.get("One_skill_classes",[]),comp.get("Two_skill_classes",[]))] or [1])
    for i,row in enumerate(comp.itertuples(index=False)):
        yy=top_y+12+i*rh
        label,fs=fit_text(row.Unit,120,7); txt(x2+12,yy+3,label,fs)
        bx=x2+142; bw=w2-165
        one=max(0,float(row.One_skill_classes)); two=max(0,float(row.Two_skill_classes))
        scale=bw/maxstack
        if one:
            c.setFillColor(C["teal"]); c.rect(bx,yy,one*scale,10,fill=1,stroke=0)
            if one*scale>15: txt(bx+one*scale/2-3,yy+2,str(int(one)),6,C["white"],True)
        if two:
            c.setFillColor(C["blue"]); c.rect(bx+one*scale,yy,two*scale,10,fill=1,stroke=0)
            if two*scale>15: txt(bx+one*scale+two*scale/2-3,yy+2,str(int(two)),6,C["white"],True)
    txt(x2+145,top_y+top_h-39,"■ One skill",7,C["teal"],True); txt(x2+220,top_y+top_h-39,"■ Two skills",7,C["blue"],True)

    panel(x3, top_y, w3, top_h, "Trainer pool")
    t=trainer_df.groupby("Trainer_Type",as_index=False)["Count_reported"].sum() if not trainer_df.empty else pd.DataFrame(columns=["Trainer_Type","Count_reported"])
    t=t[t.Count_reported>0]; total_t=float(t.Count_reported.sum()) if not t.empty else 1
    trainer_palette={"External Trainers":C["blue"],"CAPS / PhD Scholars":C["purple"],
      "Digital Computer Science Department Trainers":C["teal"],"Internal Department Trainers":C["orange"]}
    cx=x3+94; cy=top_y+top_h-91; radius=49
    start=90
    for row in t.itertuples(index=False):
        extent=360*float(row.Count_reported)/total_t
        c.setStrokeColor(trainer_palette.get(row.Trainer_Type,C["grey"])); c.setLineWidth(19)
        c.arc(cx-radius,cy-radius,cx+radius,cy+radius,start,extent)
        start+=extent
    c.setFillColor(C["white"]); c.circle(cx,cy,32,fill=1,stroke=0)
    txt(cx-16,cy+2,f"{int(total_t)}",13,C["ink"],True); txt(cx-19,cy-10,"TRAINERS",5.5,C["muted"])
    ly=top_y+top_h-153
    for row in t.itertuples(index=False):
        col=trainer_palette.get(row.Trainer_Type,C["grey"]); c.setFillColor(col); c.rect(x3+165,ly,7,7,fill=1,stroke=0)
        label,fs=fit_text(row.Trainer_Type,w3-205,6.5); txt(x3+177,ly+1,label,fs)
        txt(x3+w3-28,ly+1,str(int(row.Count_reported)),7,C["ink"],True); ly-=20

    # Lower row: all individual skill entries in two columns and UG/PG donut.
    lower_y, lower_h = 42, top_y-55
    sx, sw = margin, 735
    ux, uw = sx+sw+10, W-margin-(sx+sw+10)
    panel(sx, lower_y, sw, lower_h, "Skills delivered by type · individual source entries")
    sk=skills_df.copy()
    if not sk.empty:
        sk["Skill group"]=sk.Skill.apply(skill_group)
        sk=sk.sort_values(["Skill group","Count_reported","Skill"],ascending=[True,False,True]).reset_index(drop=True)
    half=(len(sk)+1)//2; col_w=(sw-36)/2; row_space=(lower_h-55)/max(half,1)
    for col in range(2):
        subset=sk.iloc[col*half:(col+1)*half]
        for j,row in enumerate(subset.itertuples(index=False)):
            yy=lower_y+lower_h-43-(j+1)*row_space
            color=group_colors.get(skill_group(row.Skill),C["grey"])
            c.setFillColor(color); c.circle(sx+14+col*col_w,yy+3,3,fill=1,stroke=0)
            label,fs=fit_text(row.Skill,col_w-65,6.3)
            txt(sx+23+col*col_w,yy,label,fs)
            txt(sx+col*col_w+col_w-27,yy,str(int(row.Count_reported)),6.5,C["ink"],True)
            c.setStrokeColor(colors.HexColor("#EEF1F5")); c.setLineWidth(.35)
            c.line(sx+10+col*col_w,yy-4,sx+col*col_w+col_w-10,yy-4)

    panel(ux, lower_y, uw, lower_h, "Undergraduate vs postgraduate students")
    total_level=max(ug+pg,1); cx=ux+uw*.36; cy=lower_y+lower_h*.57; r=76
    start=90
    for val,col in [(ug,C["blue"]),(pg,C["orange"])]:
        extent=360*val/total_level
        c.setStrokeColor(col); c.setLineWidth(27); c.arc(cx-r,cy-r,cx+r,cy+r,start,extent); start+=extent
    c.setFillColor(C["white"]); c.circle(cx,cy,55,fill=1,stroke=0)
    txt(cx-25,cy+5,f"{total_students:,}",15,C["ink"],True); txt(cx-22,cy-10,"STUDENTS",6,C["muted"])
    legend_x=ux+uw*.65; legend_y=cy+37
    for label,val,col in [("Undergraduate",ug,C["blue"]),("Postgraduate",pg,C["orange"])]:
        c.setFillColor(col); c.rect(legend_x,legend_y,9,9,fill=1,stroke=0)
        txt(legend_x+15,legend_y+1,label,8,C["ink"]); txt(legend_x+15,legend_y-13,f"{val:,} students",9,C["ink"],True)
        legend_y-=55
    txt(ux+16,lower_y+24,f"Total students: {total_students:,}  |  UG: {ug:,}  |  PG: {pg:,}",8,C["muted"],True)

    # Footer and concise source caveat
    c.setFillColor(C["navy"]); c.roundRect(margin, 14, W-2*margin, 20, 5, fill=1, stroke=0)
    txt(margin+12,21,"TCLS Skill Development Dashboard · Yeshwanthpur Campus · Odd Semester · AY 2026–27",7,C["white"])
    txt(W-margin-370,21,"Source: 8 updated unit documents · Reported totals; see live dashboard for data-quality notes",6.5,C["white"])
    c.showPage(); c.save()
    return buf.getvalue()


kpis=[
 (f"{filtered_students:,}","TOTAL STUDENTS REPORTED",BLUE),
 (f"{filtered_trainers:,}","TRAINERS REPORTED",PURPLE),
 (f"{filtered_classes:,}","TOTAL CLASSES REPORTED",TEAL),
 (f"{filtered_skills:,}","SKILLS DELIVERED · HEADLINE TOTAL",ORANGE)]
cols=st.columns(4,gap="small")
for c,(v,l,color) in zip(cols,kpis):
    c.markdown(f'<div class="kpi" style="border-top-color:{color}"><div class="value">{v}</div><div class="label">{l}</div></div>',unsafe_allow_html=True)

# One-page PDF export: uses the current reporting-unit filter selection.
pdf_bytes = build_dashboard_pdf(u, sf, f_completion, f_trainers, f_skills)
st.download_button(
    label="Download full dashboard as one-page PDF",
    data=pdf_bytes,
    file_name="TCLS_Yeshwanthpur_Dashboard.pdf",
    mime="application/pdf",
    use_container_width=False,
)

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
