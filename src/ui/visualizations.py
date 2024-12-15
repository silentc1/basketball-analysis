import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ..config.settings import TEAM_COLORS, COURT_ZONES

def create_shot_chart(shot_locations_df):
    """Şut haritası oluşturur"""
    fig = px.scatter(
        shot_locations_df,
        x='x',
        y='y',
        color='team',
        symbol='successful',
        color_discrete_map=TEAM_COLORS,
        title='Şut Haritası',
        labels={'x': 'X Pozisyonu', 'y': 'Y Pozisyonu'},
        height=600
    )
    
    # Saha çizgilerini ekle
    add_court_lines(fig)
    return fig

def create_heatmap(positions_data):
    """Oyuncu pozisyonlarından heatmap oluşturur"""
    figs = {}
    for team in positions_data:
        x = positions_data[team]['x']
        y = positions_data[team]['y']
        
        fig = go.Figure(go.Histogram2d(
            x=x,
            y=y,
            colorscale='Hot',
            nbinsx=20,
            nbinsy=20,
            name=team
        ))
        
        add_court_lines(fig)
        fig.update_layout(title=f'{team} Pozisyon Yoğunluğu')
        figs[team] = fig
    
    return figs

def create_stats_comparison(team_stats):
    """Takım istatistiklerini karşılaştırmalı grafik olarak gösterir"""
    stats_df = pd.DataFrame(team_stats).reset_index()
    stats_df.columns = ['Kategori', 'Takım A', 'Takım B']
    
    fig = go.Figure(data=[
        go.Bar(name='Takım A', x=stats_df['Kategori'], y=stats_df['Takım A'], marker_color=TEAM_COLORS['team_a']),
        go.Bar(name='Takım B', x=stats_df['Kategori'], y=stats_df['Takım B'], marker_color=TEAM_COLORS['team_b'])
    ])
    
    fig.update_layout(
        barmode='group',
        title='Takım İstatistikleri Karşılaştırması',
        xaxis_title='İstatistik Kategorisi',
        yaxis_title='Değer'
    )
    
    return fig

def add_court_lines(fig):
    """Basketbol sahası çizgilerini grafiğe ekler"""
    # Üç sayı çizgisi
    three_point = COURT_ZONES['three_point_line']
    fig.add_shape(type="rect",
        x0=three_point['x'][0], y0=three_point['y'][0],
        x1=three_point['x'][1], y1=three_point['y'][1],
        line=dict(color="White"),
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Boyalı alan
    paint = COURT_ZONES['paint_area']
    fig.add_shape(type="rect",
        x0=paint['x'][0], y0=paint['y'][0],
        x1=paint['x'][1], y1=paint['y'][1],
        line=dict(color="White"),
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Serbest atış çizgisi
    fig.add_shape(type="line",
        x0=paint['x'][0], y0=COURT_ZONES['free_throw_line']['y'],
        x1=paint['x'][1], y1=COURT_ZONES['free_throw_line']['y'],
        line=dict(color="White", width=2)
    ) 