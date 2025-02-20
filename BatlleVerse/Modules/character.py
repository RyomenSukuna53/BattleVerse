from BGMI import bot 
from pyrogram import filters
from pyrogram.types import Message

character_data = {
    "Yamcha": {
        "hp": "180",
        "photo": "https://files.catbox.moe/example1.jpg",
        "caption": "Yamcha is an Earthling warrior known for his Wolf Fang Fist, but he often gets outclassed in battles.",
        "base_stats": {"hp": 180, "atk": 60, "def": 50, "spe": 65, "acc": 80},
        "moves": {
            "Wolf Fang Fist": {"damage": [20, 40], "level": 1},
            "Spirit Ball": {"damage": [40, 60], "level": 20},
            "Kamehameha": {"damage": [60, 80], "level": 60},
            "Neo Wolf Fang Fist": {"damage": [80, 100], "level": 100}
        }
    },
    "Chiaotzu": {
        "hp": "150",
        "photo": "https://files.catbox.moe/example2.jpg",
        "caption": "Chiaotzu is a small psychic warrior and Tien’s best friend, but his strength is limited.",
        "base_stats": {"hp": 150, "atk": 45, "def": 40, "spe": 55, "acc": 75},
        "moves": {
            "Dodging Strike": {"damage": [15, 30], "level": 1},
            "Telekinesis": {"damage": [30, 50], "level": 20},
            "Energy Blast": {"damage": [50, 70], "level": 60},
            "Self-Destruct": {"damage": [100, 120], "level": 100}
        }
    },
    "Videl": {
        "hp": "140",
        "photo": "https://files.catbox.moe/example3.jpg",
        "caption": "Videl is a skilled martial artist and the daughter of Mr. Satan, but she lacks energy-based attacks.",
        "base_stats": {"hp": 140, "atk": 50, "def": 45, "spe": 60, "acc": 78},
        "moves": {
            "Flying Kick": {"damage": [15, 35], "level": 1},
            "Rapid Punches": {"damage": [35, 55], "level": 20},
            "Power Kick": {"damage": [55, 75], "level": 60},
            "Full Power Combo": {"damage": [75, 95], "level": 100}
        }
    },
    "Mr. Satan": {
        "hp": "200",
        "photo": "https://files.catbox.moe/example4.jpg",
        "caption": "Mr. Satan is the world champion in martial arts, but he lacks any real superhuman abilities.",
        "base_stats": {"hp": 200, "atk": 40, "def": 60, "spe": 50, "acc": 70},
        "moves": {
            "Dynamite Kick": {"damage": [10, 30], "level": 1},
            "Megaton Punch": {"damage": [30, 50], "level": 20},
            "Hero Pose": {"damage": [50, 70], "level": 60},
            "Hercule Miracle": {"damage": [70, 90], "level": 100}
        }
    },
    "Guldo": {
        "hp": "190",
        "photo": "https://files.catbox.moe/example5.jpg",
        "caption": "Guldo is a member of the Ginyu Force with psychic abilities but lacks raw power and speed.",
        "base_stats": {"hp": 190, "atk": 55, "def": 50, "spe": 45, "acc": 77},
        "moves": {
            "Eye Beam": {"damage": [20, 40], "level": 1},
            "Time Freeze": {"damage": [40, 60], "level": 20},
            "Mind Blast": {"damage": [60, 80], "level": 60},
            "Psychic Fury": {"damage": [80, 100], "level": 100}
        }
    }
}
 


