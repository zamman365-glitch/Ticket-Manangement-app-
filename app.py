"""
main.py — Streamlit entry-point.
Handles page routing, session state, and top-level layout.
Run with:  streamlit run main.py
"""

from __future__ import annotations

import streamlit as st

# ── Page config must be the FIRST Streamlit call ───────────────────────────
st.set_page_config(
    page_title="BookMyShow",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Local imports (after set_page_config) ──────────────────────────────────
from styles import inject_css
from components import (
    render_navbar,
    render_hero,
    section_header,
    movie_card,
    booking_summary,
    seat_picker_visual,
    banner_success,
    banner_error,
    banner_info,
    booking_history_card,
    empty_state,
)
from movies import get_all_movies, search_movies
from bookings import book_ticket, get_bookings_by_user

# ── Inject global CSS ──────────────────────────────────────────────────────
inject_css()


# ══════════════════════════════════════════════════════════════════════════════
# Session State Defaults
# ══════════════════════════════════════════════════════════════════════════════

def _init_state() -> None:
    defaults = {
        "user_id": None,
        "page": "home",            # home | book | my_bookings
        "selected_movie": None,
        "booking_done": False,
        "last_booking_id": None,
        "search_query": "",
        "genre_filter": "All",
        "lang_filter": "All",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ══════════════════════════════════════════════════════════════════════════════
# Sidebar — Login + Filters
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar() -> None:
    with st.sidebar:
        # ── User login ────────────────────────────────────────────────────
        st.markdown("### 👤 Account")

        if st.session_state.user_id is None:
            uid = st.number_input(
                "Enter your User ID to log in",
                min_value=1,
                step=1,
                format="%d",
                key="login_uid",
            )
            if st.button("Sign In", key="btn_login"):
                st.session_state.user_id = int(uid)
                st.success(f"Welcome, User #{uid}! 🎉")
                st.rerun()
        else:
            st.markdown(
                f"""
                <div style="background:var(--bg-elevated);border:1px solid var(--border);
                            border-radius:8px;padding:14px;margin-bottom:16px;">
                    <div style="font-size:12px;color:var(--text-muted);">Logged in as</div>
                    <div style="font-size:16px;font-weight:700;color:var(--text-primary);">
                        User #{st.session_state.user_id}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎟 My Bookings", key="btn_mybookings"):
                    st.session_state.page = "my_bookings"
                    st.rerun()
            with col2:
                if st.button("Sign Out", key="btn_logout"):
                    for k in ["user_id", "selected_movie", "booking_done"]:
                        st.session_state[k] = None if k != "booking_done" else False
                    st.session_state.page = "home"
                    st.rerun()

        st.divider()

        # ── Filters ───────────────────────────────────────────────────────
        st.markdown("### 🎛 Filters")

        st.session_state.search_query = st.text_input(
            "🔍 Search movies",
            value=st.session_state.search_query,
            placeholder="Title, genre, language…",
        )

        # Dynamic filter options
        all_movies = get_all_movies()
        genres  = ["All"] + sorted({m["genre"] for m in all_movies if m.get("genre")})
        langs   = ["All"] + sorted({m["language"] for m in all_movies if m.get("language")})

        st.session_state.genre_filter = st.selectbox(
            "Genre", genres,
            index=genres.index(st.session_state.genre_filter)
            if st.session_state.genre_filter in genres else 0,
        )
        st.session_state.lang_filter = st.selectbox(
            "Language", langs,
            index=langs.index(st.session_state.lang_filter)
            if st.session_state.lang_filter in langs else 0,
        )

        st.divider()
        if st.button("🏠 Home", key="btn_home"):
            st.session_state.page = "home"
            st.session_state.selected_movie = None
            st.session_state.booking_done = False
            st.rerun()

        # ── Stats ─────────────────────────────────────────────────────────
        st.divider()
        st.markdown("### 📊 Stats")
        total = len(all_movies)
        available = sum(1 for m in all_movies if (m.get("available_seats") or 0) > 0)
        st.metric("Total Movies", total)
        st.metric("Seats Available", available)


# ══════════════════════════════════════════════════════════════════════════════
# Page: Home — Movie Listing
# ══════════════════════════════════════════════════════════════════════════════

def page_home() -> None:
    all_movies = get_all_movies()

    # Apply search
    query = st.session_state.search_query.strip()
    movies = search_movies(query) if query else all_movies

    # Apply filters
    if st.session_state.genre_filter != "All":
        movies = [m for m in movies if m.get("genre") == st.session_state.genre_filter]
    if st.session_state.lang_filter != "All":
        movies = [m for m in movies if m.get("language") == st.session_state.lang_filter]

    render_hero(len(movies))

    if not movies:
        empty_state("🎭", "No movies found", "Try adjusting your search or filters.")
        return

    section_header("NOW SHOWING", f"{len(movies)} films")

    # 4-column grid
    cols_per_row = 4
    for row_start in range(0, len(movies), cols_per_row):
        row_movies = movies[row_start : row_start + cols_per_row]
        cols = st.columns(cols_per_row, gap="medium")
        for col, movie in zip(cols, row_movies):
            with col:
                movie_card(movie)
                is_sold_out = (movie.get("available_seats") or 0) == 0
                btn_label = "HOUSEFULL 🔴" if is_sold_out else "BOOK TICKETS"
                if st.button(
                    btn_label,
                    key=f"book_{movie['movie_id']}",
                    disabled=is_sold_out,
                ):
                    if st.session_state.user_id is None:
                        st.warning("⚠️ Please sign in first (sidebar).")
                    else:
                        st.session_state.selected_movie = movie
                        st.session_state.page = "book"
                        st.session_state.booking_done = False
                        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# Page: Book Ticket
# ══════════════════════════════════════════════════════════════════════════════

def page_book() -> None:
    movie = st.session_state.selected_movie

    # safety check
    if not movie:
        st.session_state.page = "home"
        st.rerun()

    # Back button
    if st.button("← Back to Movies", key="btn_back"):
        st.session_state.page = "home"
        st.session_state.selected_movie = None
        st.rerun()

    # Booking success screen
    if st.session_state.booking_done:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="text-align:center;padding:40px 20px;">
                <div style="font-size:80px;margin-bottom:16px;">🎉</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:42px;
                            color:var(--success);letter-spacing:2px;">
                    BOOKING CONFIRMED!
                </div>
                <div style="color:var(--text-secondary);font-size:15px;margin-top:8px;">
                    Booking #<strong style="color:var(--text-primary)">
                    {st.session_state.last_booking_id}</strong>
                    · Your tickets are reserved.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 Browse More Movies", key="btn_moremovies"):
                st.session_state.page = "home"
                st.session_state.selected_movie = None
                st.session_state.booking_done = False
                st.rerun()

            if st.button("📋 View My Bookings", key="btn_view_bookings"):
                st.session_state.page = "my_bookings"
                st.session_state.booking_done = False
                st.rerun()

        return

    # Layout
    left, right = st.columns([3, 2], gap="large")

    with left:
        section_header("MOVIE DETAILS")

        # Poster
        pcol, icol = st.columns([1, 2], gap="medium")

        with pcol:
            poster = movie.get("poster_url", "")
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.markdown(
                    '<div class="movie-poster-placeholder">🎬</div>',
                    unsafe_allow_html=True,
                )

        # Movie info
        with icol:
            st.markdown(
                f"""
                <div style="padding-top:8px;">
                    <h1 style="font-family:'Bebas Neue',sans-serif;font-size:36px;
                               color:var(--text-primary);margin:0 0 12px;letter-spacing:2px;">
                        {movie.get('movie_name', 'No Title')}
                    </h1>

                    <div class="movie-meta" style="margin-bottom:14px;">
                        <span class="tag tag-genre">{movie.get('genre','')}</span>
                        <span class="tag tag-lang">{movie.get('language','')}</span>
                        <span class="tag tag-rating">⭐ {movie.get('rating','U/A')}</span>
                        <span class="tag">🕐 {movie.get('duration_mins','')} min</span>
                    </div>

                    <p style="color:var(--text-secondary);font-size:14px;line-height:1.7;margin-bottom:16px;">
                        {movie.get('description') or 'No description available.'}
                    </p>

                    <div style="font-size:13px;color:var(--text-muted);">
                        🗓 Release:
                        <strong style="color:var(--text-primary);">
                            {movie.get('release_date','')}
                        </strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Seat map
        section_header("SELECT YOUR SEATS")
        total_seats = movie.get("total_seats", 60) or 60
        avail_seats = movie.get("available_seats", 0) or 0
        booked_seats = total_seats - avail_seats

        seat_picker_visual(total=total_seats, booked=booked_seats)

    with right:
        st.markdown('<div class="booking-panel">', unsafe_allow_html=True)
        st.markdown('<div class="booking-panel-title">CONFIRM BOOKING</div>', unsafe_allow_html=True)

        banner_info(f"Logged in as User #{st.session_state.user_id}")

        # 🚨 IMPORTANT FIX: prevent crash when no seats
        if avail_seats < 1:
            banner_error("❌ Housefull! No seats available.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        max_seats = min(10, avail_seats)

        seats = st.slider(
            "Number of seats",
            min_value=1,
            max_value=max_seats,
            value=1,
            key="seats_slider",
        )

        booking_summary(movie, seats)

        if st.button("🎟 PAY & CONFIRM", key="btn_confirm_booking"):
            result = book_ticket(
                user_id=st.session_state.user_id,
                movie_id=movie.get("movie_id"),
                seats=seats,
            )

            if result.success:
                st.session_state.booking_done = True
                st.session_state.last_booking_id = result.booking_id
                st.session_state.selected_movie = None
                st.rerun()
            else:
                banner_error(result.message)

        st.markdown("</div>", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# Page: My Bookings
# ══════════════════════════════════════════════════════════════════════════════

def page_my_bookings() -> None:
    if st.session_state.user_id is None:
        banner_info("Please sign in to view your bookings.")
        return

    if st.button("← Back", key="btn_back_hist"):
        st.session_state.page = "home"
        st.rerun()

    section_header("MY BOOKINGS", f"User #{st.session_state.user_id}")

    bookings = get_bookings_by_user(st.session_state.user_id)

    if not bookings:
        empty_state("🎟", "No bookings yet", "Book your first ticket to see it here!")
        return

    # Summary metrics
    total_spent = sum(b.get("total_amount", 0) for b in bookings)
    total_seats = sum(b.get("seats_booked", 0) for b in bookings)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Bookings", len(bookings))
    m2.metric("Seats Booked", total_seats)
    m3.metric("Total Spent", f"₹{total_spent}")

    st.markdown("<br>", unsafe_allow_html=True)

    for b in bookings:
        booking_history_card(b)


# ══════════════════════════════════════════════════════════════════════════════
# Router
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    render_navbar()
    render_sidebar()

    page = st.session_state.get("page", "home")

    if page == "home":
        page_home()
    elif page == "book":
        page_book()
    elif page == "my_bookings":
        page_my_bookings()
    else:
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    main()
