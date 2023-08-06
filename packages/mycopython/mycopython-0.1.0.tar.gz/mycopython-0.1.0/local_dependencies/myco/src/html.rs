use crate::blocks;
use build_html::{Container, ContainerType, Html, HtmlContainer};
pub fn block_to_tag(block: &blocks::Block) {
    let mut container = Container::default();
    match block.t {
        blocks::BlockType::Paragraph => {
            let mut paragraph = format!("");
            for line in &block.lines {
                for span in &line.spans {
                    paragraph.push_str(&span.to_html_string());
                    // &span.to_html_string()
                }
            }
            container.add_paragraph(&paragraph);
        }
    };
    let html = container.to_html_string();
    log::debug!("{:?}", block);
    log::info!("{}", html);
}
