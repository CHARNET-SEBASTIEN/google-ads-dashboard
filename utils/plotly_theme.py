"""
Configuration Plotly pour le thème RAFO dark mode
"""

# Thème RAFO pour les graphiques Plotly
RAFO_DARK_THEME = {
    'layout': {
        'paper_bgcolor': '#1a1a1a',  # Fond du graphique
        'plot_bgcolor': '#1a1a1a',   # Fond de la zone de tracé
        'font': {
            'color': '#ffffff',
            'family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'size': 12
        },
        'xaxis': {
            'gridcolor': '#2a2a2a',
            'linecolor': '#2a2a2a',
            'tickcolor': '#a0a0a0',
            'tickfont': {'color': '#a0a0a0'},
            'titlefont': {'color': '#ffffff'}
        },
        'yaxis': {
            'gridcolor': '#2a2a2a',
            'linecolor': '#2a2a2a',
            'tickcolor': '#a0a0a0',
            'tickfont': {'color': '#a0a0a0'},
            'titlefont': {'color': '#ffffff'}
        },
        'title': {
            'font': {
                'color': '#ffffff',
                'size': 16,
                'family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            }
        },
        'legend': {
            'font': {'color': '#ffffff'},
            'bgcolor': '#141414',
            'bordercolor': '#2a2a2a'
        },
        'colorway': [
            '#f59e0b',  # Orange (accent)
            '#3b82f6',  # Bleu
            '#10b981',  # Vert
            '#ef4444',  # Rouge
            '#8b5cf6',  # Violet
            '#f97316',  # Orange foncé
            '#06b6d4',  # Cyan
            '#ec4899'   # Rose
        ],
        'hovermode': 'x unified',
        'hoverlabel': {
            'bgcolor': '#141414',
            'bordercolor': '#f59e0b',
            'font': {'color': '#ffffff'}
        }
    }
}

# Thème clair (défaut)
RAFO_LIGHT_THEME = {
    'layout': {
        'paper_bgcolor': '#ffffff',
        'plot_bgcolor': '#ffffff',
        'font': {
            'color': '#1a1a1a',
            'family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'size': 12
        },
        'xaxis': {
            'gridcolor': '#e5e7eb',
            'linecolor': '#e5e7eb',
            'tickcolor': '#6b7280',
            'tickfont': {'color': '#6b7280'},
            'titlefont': {'color': '#1a1a1a'}
        },
        'yaxis': {
            'gridcolor': '#e5e7eb',
            'linecolor': '#e5e7eb',
            'tickcolor': '#6b7280',
            'tickfont': {'color': '#6b7280'},
            'titlefont': {'color': '#1a1a1a'}
        },
        'title': {
            'font': {
                'color': '#1a1a1a',
                'size': 16
            }
        },
        'legend': {
            'font': {'color': '#1a1a1a'},
            'bgcolor': '#f9fafb',
            'bordercolor': '#e5e7eb'
        },
        'colorway': [
            '#f59e0b',  # Orange
            '#3b82f6',  # Bleu
            '#10b981',  # Vert
            '#ef4444',  # Rouge
            '#8b5cf6',  # Violet
            '#f97316',
            '#06b6d4',
            '#ec4899'
        ]
    }
}


def apply_rafo_theme(fig, dark_mode=True):
    """
    Applique le thème RAFO à un graphique Plotly

    Args:
        fig: Figure Plotly
        dark_mode: True pour thème sombre, False pour thème clair

    Returns:
        Figure avec thème appliqué
    """
    theme = RAFO_DARK_THEME if dark_mode else RAFO_LIGHT_THEME

    fig.update_layout(**theme['layout'])

    # Style supplémentaire
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        showlegend=True
    )

    return fig


def get_rafo_colors(dark_mode=True):
    """
    Retourne la palette de couleurs RAFO

    Args:
        dark_mode: True pour thème sombre, False pour thème clair

    Returns:
        Liste de couleurs
    """
    theme = RAFO_DARK_THEME if dark_mode else RAFO_LIGHT_THEME
    return theme['layout']['colorway']
