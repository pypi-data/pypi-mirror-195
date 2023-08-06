#[derive(Debug)]
pub enum Link {
    Url(String),
    WikilinkTarget(String),
}

#[derive(Debug)]
pub struct Wikilink {
    pub target: Link,
    pub title: String,
}

#[derive(Debug)]
pub struct Inlinelink {
    pub target: Link,
    pub title: String,
}

#[derive(Debug)]
pub struct PlainText {
    pub content: String,
}

#[derive(Debug)]
pub enum Style {
    Italic,
}
#[derive(Debug)]
pub struct FormattedText {
    pub style: Style,
    pub content: String,
}
#[derive(Debug)]
pub struct Code {
    pub content: String,
}

pub trait Paragraph: std::fmt::Debug {
    fn to_html(&self) -> String;
}

impl Paragraph for PlainText {
    fn to_html(&self) -> String {
        format!("{} ", &self.content)
    }
}

impl Paragraph for Wikilink {
    fn to_html(&self) -> String {
        let link = match &self.target {
            Link::WikilinkTarget(link) => link,
            Link::Url(link) => link,
        };
        let mut title = &self.title;
        if title == "" {
            title = link;
        }
        format!("<a href='{}'>{}</a> ", link, title)
    }
}

// Same as Wikilink, separating because I might change format someday
impl Paragraph for Inlinelink {
    fn to_html(&self) -> String {
        let link = match &self.target {
            Link::WikilinkTarget(link) => link,
            Link::Url(link) => link,
        };
        let mut title = &self.title;
        if title == "" {
            title = link;
        }
        format!("<a href='{}'>{}</a> ", link.trim(), title)
    }
}

impl Paragraph for FormattedText {
    fn to_html(&self) -> String {
        let tag = match self.style {
            Style::Italic => "em",
        };
        format!("<{}>{}</{}> ", tag, self.content, tag)
    }
}

impl Paragraph for Code {
    fn to_html(&self) -> String {
        format!("<pre>{}</pre>", self.content)
    }
}
