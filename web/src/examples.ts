import type { QueueSample } from './apps/queue';
import type { ChatSample } from './apps/chat';

export const routingExamples: QueueSample[] = [
  {
    "id": "demo-s1:sorter-07:described",
    "state": "I've got three paragraphs announcing our neighborhood swap day. Help make them warmer and less repetitive while keeping the practical details intact.",
    "question": "Which workspace best fits this request?",
    "options": [
      {
        "id": "sorter-07",
        "text": "Visual canvas: A workspace for arranging images, colors, shapes, and layouts into visual compositions.",
        "label": "Design"
      },
      {
        "id": "sorter-08",
        "text": "Schedule planner: A workspace for arranging activities into available dates, times, and durations.",
        "label": "Scheduling"
      },
      {
        "id": "sorter-05",
        "text": "Writing desk: A workspace for drafting, revising, and polishing prose for different audiences.",
        "label": "Writing"
      },
      {
        "id": "sorter-06",
        "text": "Number sheet: A workspace for organizing numerical data, calculating totals, and comparing quantities.",
        "label": "Numbers"
      }
    ],
    "title": "Polish the swap-day announcement"
  },
  {
    "id": "demo-s1:sorter-08:described",
    "state": "We have three activities for Saturday, and everyone is free at different times. Help find a sensible order and put each activity into a slot that works for the group.",
    "question": "Which workspace best fits this request?",
    "options": [
      {
        "id": "sorter-08",
        "text": "Schedule planner: A workspace for arranging activities into available dates, times, and durations.",
        "label": "Scheduling"
      },
      {
        "id": "sorter-05",
        "text": "Writing desk: A workspace for drafting, revising, and polishing prose for different audiences.",
        "label": "Writing"
      },
      {
        "id": "sorter-06",
        "text": "Number sheet: A workspace for organizing numerical data, calculating totals, and comparing quantities.",
        "label": "Numbers"
      },
      {
        "id": "sorter-07",
        "text": "Visual canvas: A workspace for arranging images, colors, shapes, and layouts into visual compositions.",
        "label": "Design"
      }
    ],
    "title": "Plan Saturday together"
  },
  {
    "id": "demo-s1:sorter-09:described",
    "state": "Here are the quantities and unit prices for our picnic supplies. Work out the overall cost and how much each of the eight people would contribute.",
    "question": "Which workspace best fits this request?",
    "options": [
      {
        "id": "sorter-05",
        "text": "Writing desk: A workspace for drafting, revising, and polishing prose for different audiences.",
        "label": "Writing"
      },
      {
        "id": "sorter-06",
        "text": "Number sheet: A workspace for organizing numerical data, calculating totals, and comparing quantities.",
        "label": "Numbers"
      },
      {
        "id": "sorter-07",
        "text": "Visual canvas: A workspace for arranging images, colors, shapes, and layouts into visual compositions.",
        "label": "Design"
      },
      {
        "id": "sorter-08",
        "text": "Schedule planner: A workspace for arranging activities into available dates, times, and durations.",
        "label": "Scheduling"
      }
    ],
    "title": "Split the picnic budget"
  },
  {
    "id": "demo-s1:sorter-10:described",
    "state": "I have a title, two photos, and a small logo for the club flyer. Try a few arrangements with more breathing room around the pictures.",
    "question": "Which workspace best fits this request?",
    "options": [
      {
        "id": "sorter-06",
        "text": "Number sheet: A workspace for organizing numerical data, calculating totals, and comparing quantities.",
        "label": "Numbers"
      },
      {
        "id": "sorter-07",
        "text": "Visual canvas: A workspace for arranging images, colors, shapes, and layouts into visual compositions.",
        "label": "Design"
      },
      {
        "id": "sorter-08",
        "text": "Schedule planner: A workspace for arranging activities into available dates, times, and durations.",
        "label": "Scheduling"
      },
      {
        "id": "sorter-05",
        "text": "Writing desk: A workspace for drafting, revising, and polishing prose for different audiences.",
        "label": "Writing"
      }
    ],
    "title": "Give the club flyer more space"
  },
  {
    "id": "demo-s1:sorter-11:described",
    "state": "Turn these workshop sessions into a one-page timetable. The times are fixed already; what I mainly need is a clear arrangement of blocks that people can scan quickly.",
    "question": "Which workspace best fits the main work requested?",
    "options": [
      {
        "id": "sorter-07",
        "text": "Visual canvas: A workspace for arranging images, colors, shapes, and layouts into visual compositions.",
        "label": "Design"
      },
      {
        "id": "sorter-08",
        "text": "Schedule planner: A workspace for arranging activities into available dates, times, and durations.",
        "label": "Scheduling"
      },
      {
        "id": "sorter-05",
        "text": "Writing desk: A workspace for drafting, revising, and polishing prose for different audiences.",
        "label": "Writing"
      },
      {
        "id": "sorter-06",
        "text": "Number sheet: A workspace for organizing numerical data, calculating totals, and comparing quantities.",
        "label": "Numbers"
      }
    ],
    "title": "Lay out the workshop timetable"
  },
  {
    "id": "demo-s1:sorter-12:described",
    "state": "Help map out Saturday's baking session. Each batch needs different oven time, and I also want to see how many batches we can finish before noon.",
    "question": "Which workspace best fits this request?",
    "options": [
      {
        "id": "sorter-08",
        "text": "Schedule planner: A workspace for arranging activities into available dates, times, and durations.",
        "label": "Scheduling"
      },
      {
        "id": "sorter-05",
        "text": "Writing desk: A workspace for drafting, revising, and polishing prose for different audiences.",
        "label": "Writing"
      },
      {
        "id": "sorter-06",
        "text": "Number sheet: A workspace for organizing numerical data, calculating totals, and comparing quantities.",
        "label": "Numbers"
      },
      {
        "id": "sorter-07",
        "text": "Visual canvas: A workspace for arranging images, colors, shapes, and layouts into visual compositions.",
        "label": "Design"
      }
    ],
    "title": "Fit the baking into one morning"
  }
];

export const sentimentExamples: ChatSample[] = [
  {
    "id": "demo-s2:sentiment-01",
    "state": "I love how bright the kitchen feels after we painted it.",
    "question": "What sentiment does this message express?",
    "options": [
      {
        "id": "positive",
        "text": "Positive: favorable feelings or assessment, without meaningful negative sentiment.",
        "label": "Positive",
        "emoji": "🎉"
      },
      {
        "id": "negative",
        "text": "Negative: unfavorable feelings or assessment, without meaningful positive sentiment.",
        "label": "Negative",
        "emoji": "💛"
      },
      {
        "id": "neutral",
        "text": "Neutral: information or a question without positive or negative feelings.",
        "label": "Neutral",
        "emoji": "👍"
      },
      {
        "id": "mixed",
        "text": "Mixed: both favorable and unfavorable feelings or assessments.",
        "label": "Mixed",
        "emoji": "🤔"
      }
    ]
  },
  {
    "id": "demo-s2:sentiment-02",
    "state": "I'm frustrated that the payroll error still hasn't been fixed.",
    "question": "What sentiment does this message express?",
    "options": [
      {
        "id": "positive",
        "text": "Positive: favorable feelings or assessment, without meaningful negative sentiment.",
        "label": "Positive",
        "emoji": "🎉"
      },
      {
        "id": "negative",
        "text": "Negative: unfavorable feelings or assessment, without meaningful positive sentiment.",
        "label": "Negative",
        "emoji": "💛"
      },
      {
        "id": "neutral",
        "text": "Neutral: information or a question without positive or negative feelings.",
        "label": "Neutral",
        "emoji": "👍"
      },
      {
        "id": "mixed",
        "text": "Mixed: both favorable and unfavorable feelings or assessments.",
        "label": "Mixed",
        "emoji": "🤔"
      }
    ]
  },
  {
    "id": "demo-s2:sentiment-03",
    "state": "Does the library close at six on Fridays?",
    "question": "What sentiment does this message express?",
    "options": [
      {
        "id": "positive",
        "text": "Positive: favorable feelings or assessment, without meaningful negative sentiment.",
        "label": "Positive",
        "emoji": "🎉"
      },
      {
        "id": "negative",
        "text": "Negative: unfavorable feelings or assessment, without meaningful positive sentiment.",
        "label": "Negative",
        "emoji": "💛"
      },
      {
        "id": "neutral",
        "text": "Neutral: information or a question without positive or negative feelings.",
        "label": "Neutral",
        "emoji": "👍"
      },
      {
        "id": "mixed",
        "text": "Mixed: both favorable and unfavorable feelings or assessments.",
        "label": "Mixed",
        "emoji": "🤔"
      }
    ]
  },
  {
    "id": "demo-s2:sentiment-04",
    "state": "I enjoyed the concert, but I'm annoyed by the extra booking fee.",
    "question": "What sentiment does this message express?",
    "options": [
      {
        "id": "positive",
        "text": "Positive: favorable feelings or assessment, without meaningful negative sentiment.",
        "label": "Positive",
        "emoji": "🎉"
      },
      {
        "id": "negative",
        "text": "Negative: unfavorable feelings or assessment, without meaningful positive sentiment.",
        "label": "Negative",
        "emoji": "💛"
      },
      {
        "id": "neutral",
        "text": "Neutral: information or a question without positive or negative feelings.",
        "label": "Neutral",
        "emoji": "👍"
      },
      {
        "id": "mixed",
        "text": "Mixed: both favorable and unfavorable feelings or assessments.",
        "label": "Mixed",
        "emoji": "🤔"
      }
    ]
  },
  {
    "id": "demo-s2:sentiment-13",
    "state": "I couldn't be happier with the repair; the bike rides beautifully.",
    "question": "What sentiment does this message express?",
    "options": [
      {
        "id": "mixed",
        "text": "Mixed: both favorable and unfavorable feelings or assessments.",
        "label": "Mixed",
        "emoji": "🤔"
      },
      {
        "id": "positive",
        "text": "Positive: favorable feelings or assessment, without meaningful negative sentiment.",
        "label": "Positive",
        "emoji": "🎉"
      },
      {
        "id": "negative",
        "text": "Negative: unfavorable feelings or assessment, without meaningful positive sentiment.",
        "label": "Negative",
        "emoji": "💛"
      },
      {
        "id": "neutral",
        "text": "Neutral: information or a question without positive or negative feelings.",
        "label": "Neutral",
        "emoji": "👍"
      }
    ]
  },
  {
    "id": "demo-s2:sentiment-14",
    "state": "With respect, I'm deeply unhappy with how you handled my complaint.",
    "question": "What sentiment does this message express?",
    "options": [
      {
        "id": "mixed",
        "text": "Mixed: both favorable and unfavorable feelings or assessments.",
        "label": "Mixed",
        "emoji": "🤔"
      },
      {
        "id": "positive",
        "text": "Positive: favorable feelings or assessment, without meaningful negative sentiment.",
        "label": "Positive",
        "emoji": "🎉"
      },
      {
        "id": "negative",
        "text": "Negative: unfavorable feelings or assessment, without meaningful positive sentiment.",
        "label": "Negative",
        "emoji": "💛"
      },
      {
        "id": "neutral",
        "text": "Neutral: information or a question without positive or negative feelings.",
        "label": "Neutral",
        "emoji": "👍"
      }
    ]
  }
];
