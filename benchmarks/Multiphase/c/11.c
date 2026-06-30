int main(){
    int x, y, z;

    // pre-conditions
    assume(x < 0);
    assume(y > 0);
    assume(((z == 0) || (z == 1)));

    // loop body
    while(unknown()){
        if(x % 2 == z){
            y = y + 2;
        }
        x = x + 1;
    }

    // post-condition
    if(x > 54932){
        assert(y > 54932);
    }
    
}