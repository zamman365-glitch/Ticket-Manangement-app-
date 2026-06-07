"""
components.py — Reusable Streamlit UI components.
Each function returns/renders a specific piece of UI.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


# ── Navbar ─────────────────────────────────────────────────────────────────

def render_navbar(city: str = "Mumbai") -> None:
    st.markdown(
        f"""
        <div class="bms-navbar">
            <div class="bms-logo">BOOK<span>MY</span>SHOW</div>
            <div class="bms-nav-pills">
                <span class="bms-pill active">🎬 Movies</span>
                <span class="bms-pill">🎭 Events</span>
                <span class="bms-pill">🏟 Sports</span>
            </div>
            <div style="color:var(--text-secondary);font-size:13px;">
                📍 {city}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Hero ────────────────────────────────────────────────────────────────────

def render_hero(movie_count: int = 0) -> None:
    st.markdown(
        f"""
        <div class="bms-hero">
            <div class="bms-hero-title">BOOK YOUR <em>PERFECT</em> SHOW</div>
            <p class="bms-hero-sub">
                {movie_count} movies now showing · Instant confirmation · Best seats guaranteed
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Section Header ──────────────────────────────────────────────────────────

def section_header(title: str, badge: str | None = None) -> None:
    badge_html = f'<span class="bms-badge">{badge}</span>' if badge else ""
    st.markdown(
        f"""
        <div class="bms-section-header">
            <h2>{title}</h2>
            {badge_html}
            <div class="bms-section-line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Movie Card ──────────────────────────────────────────────────────────────
def movie_card(movie: dict[str, Any]) -> None:
    """Renders a BookMyShow-style movie card."""


    seats = movie.get("available_seats", 0)
    total = movie.get("total_seats", 1) or 1
    occupancy = seats / total if total else 0

    # Seat status logic
    if seats == 0:
        seats_class, seats_label = "sold", "Housefull 🔴"
    elif occupancy < 0.2:
        seats_class, seats_label = "low", f"🔥 Only {seats} left"
    else:
        seats_class, seats_label = "", f"{seats} seats available"

    price = movie.get("ticket_price", 0)
    rating = movie.get("rating", "U/A")
    poster = movie.get("poster_url", "")
    duration = movie.get("duration_mins", "")

    # Poster handling (FIXED safe quotes)
    if poster:
        poster_html = f'''
            <img class="movie-poster"
                 src="{poster}"
                 alt="{movie.get("movie_name", "No Title")}"
                 loading="lazy"/>
        '''
    else:
        poster_html = '<div class="movie-poster-placeholder">🎬</div>'

    duration_str = f"{duration} min" if duration else ""

    st.markdown(
        f"""
        <div class="movie-card">
            {poster_html}
            <div class="movie-info">

                <p class="movie-title"
                   title="{movie.get('movie_name', 'No Title')}">
                   {movie.get('movie_name', 'No Title')}
                </p>

                <div class="movie-meta">
                    <span class="tag tag-genre">{movie.get('genre','')}</span>
                    <span class="tag tag-lang">{movie.get('language','')}</span>
                    <span class="tag tag-rating">⭐ {rating}</span>
                    {f'<span class="tag">{duration_str}</span>' if duration_str else ''}
                </div>

                <p class="movie-seats {seats_class}">
                    {seats_label}
                </p>

                <div class="movie-price">
                    ₹{price} <span>/ seat</span>
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Booking Summary ─────────────────────────────────────────────────────────

def booking_summary(movie: dict[str, Any], seats: int) -> None:
    price = movie.get("ticket_price", 0)
    convenience_fee = round(seats * price * 0.02)
    total = seats * price + convenience_fee

    st.markdown(
        f"""
        <div class="booking-summary">
            <div class="summary-row">
                <span>Movie</span>
                <span class="val">{movie['title']}</span>
            </div>
            <div class="summary-row">
                <span>Tickets × {seats}</span>
                <span class="val">₹{seats * price}</span>
            </div>
            <div class="summary-row">
                <span>Convenience Fee</span>
                <span class="val">₹{convenience_fee}</span>
            </div>
            <div class="summary-total">
                <span>Total Payable</span>
                <span class="amount">₹{total}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Seat Picker ─────────────────────────────────────────────────────────────

def seat_picker_visual(total: int = 60, booked: int = 0) -> None:
    """Renders a decorative seat map (visual only — actual count via slider)."""
    import random

    random.seed(booked)
    taken_indices = random.sample(range(total), min(booked, total))

    rows_per_row = 10
    num_rows = total // rows_per_row
    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    rows_html = ""
    idx = 0
    for r in range(num_rows):
        row_html = f'<span style="font-size:10px;color:var(--text-muted);margin-right:6px;width:14px;display:inline-block;">{labels[r]}</span>'
        for _ in range(rows_per_row):
            cls = "seat taken" if idx in taken_indices else "seat"
            row_html += f'<div class="{cls}"></div>'
            idx += 1
        rows_html += f'<div class="seat-row" style="align-items:center;">{row_html}</div>'

    st.markdown(
        f"""
        <div class="seat-grid">
            <div class="seat-screen"></div>
            {rows_html}
            <div class="seat-legend">
                <div><span class="legend-dot" style="background:var(--bg-elevated);border:1px solid var(--border);"></span> Available</div>
                <div><span class="legend-dot" style="background:var(--bms-red);"></span> Selected</div>
                <div><span class="legend-dot" style="background:#2a2a2a;opacity:0.5;"></span> Booked</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Banners ─────────────────────────────────────────────────────────────────

def banner_success(msg: str) -> None:
    st.markdown(
        f'<div class="banner banner-success">✅ {msg}</div>',
        unsafe_allow_html=True,
    )


def banner_error(msg: str) -> None:
    st.markdown(
        f'<div class="banner banner-error">❌ {msg}</div>',
        unsafe_allow_html=True,
    )


def banner_info(msg: str) -> None:
    st.markdown(
        f'<div class="banner banner-info">ℹ️ {msg}</div>',
        unsafe_allow_html=True,
    )


# ── Booking History Card ────────────────────────────────────────────────────

def booking_history_card(b: dict[str, Any]) -> None:
    booked_time = b.get("booking_time", "")
    if booked_time:
        try:
            booked_time = booked_time.strftime("%d %b %Y, %I:%M %p")
        except AttributeError:
            booked_time = str(booked_time)

    st.markdown(
        f"""
        <div class="history-card">
            <div>
                <p class="history-movie-name">🎬 {b['title']}</p>
                <div class="history-meta">
                    <span>🎭 {b.get('genre','')}</span>
                    <span>🌐 {b.get('language','')}</span>
                    <span>🕐 {booked_time}</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div class="history-amount">₹{b.get('total_amount', 0)}</div>
                <div class="history-seats">{b.get('seats_booked', 0)} seat(s)</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Empty State ─────────────────────────────────────────────────────────────

def empty_state(emoji: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div style="text-align:center;padding:60px 20px;color:var(--text-muted);">
            <div style="font-size:64px;margin-bottom:16px;">{emoji}</div>
            <h3 style="color:var(--text-secondary);font-family:'DM Sans',sans-serif;
                       font-weight:600;margin-bottom:8px;">{title}</h3>
            <p style="font-size:14px;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
