#!/bin/bash
ffmpeg -i movie.mp4 -i movie_music.mp3 -codec copy -shortest full_movie.mp4


